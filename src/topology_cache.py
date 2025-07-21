import pickle
import types
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.panel import Panel
from rich.console import Console, Group
from rich.text import Text
from rich.live import Live
from rich.align import Align
import os

class TopologyCache:
    def __init__(self, api_client, cache_file='topology_cache.pkl'):
        self.api_client = api_client
        self.cache_file = cache_file
        self.computers = {}
        self.network_equipments = {}
        self.passive_devices = {}
        self.cables = {}
        self.sockets = {}
        self.network_ports = {}
        self.equipment_to_sockets_map = {}
        self.changelog = []
        self.console = None

    def __getstate__(self):
        """Exclut les attributs non sérialisables de la sauvegarde pickle."""
        state = self.__dict__.copy()
        # Retirer les entrées non sérialisables.
        if 'api_client' in state:
            del state['api_client']
        if 'console' in state:
            del state['console']
        return state

    def __setstate__(self, state):
        """Restaure l'instance après la désérialisation."""
        self.__dict__.update(state)
        # Rajouter les attributs non sérialisés.
        self.api_client = None
        self.console = None

    def _clear_data(self):
        """Vide tous les dictionnaires de données du cache."""
        self.computers.clear()
        self.network_equipments.clear()
        self.passive_devices.clear()
        self.cables.clear()
        self.sockets.clear()
        self.network_ports.clear()
        self.equipment_to_sockets_map.clear()

    def load_from_api(self, console, live=None, panel=None, display_group=None):
        # ÉTAPE 1: Vider l'état actuel
        self._clear_data()

        # ÉTAPE 2: Remplir avec les nouvelles données
        self.console = console

        # --- Gestion de l'affichage --- 
        # Si un objet Live n'est pas fourni, on en crée un pour cette méthode.
        manage_live = live is None
        if manage_live:
            display_group = Group()
            panel = Panel(display_group, border_style="blue", title="[bold blue]GLPI Explorer[/bold blue]", expand=False)
            live = Live(panel, console=console, screen=True, redirect_stderr=False, vertical_overflow="visible")
            live.start()

        progress_bar = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        )
        
        main_task = progress_bar.add_task("Chargement de la topologie...", total=6)
        if display_group:
            display_group.renderables.append(progress_bar)
        if panel:
            live.update(panel)

        # --- Chargement des données ---
        self._load_computers(progress_bar, main_task, live, panel, display_group)
        self._load_network_equipments(progress_bar, main_task, live, panel, display_group)
        self._load_passive_devices(progress_bar, main_task, live, panel, display_group)
        self._load_cables(progress_bar, main_task, live, panel, display_group)
        self._load_sockets(progress_bar, main_task, live, panel, display_group)
        self._load_network_ports(progress_bar, main_task, live, panel, display_group)
        
        # --- Finalisation ---
        if display_group:
            status_text = Text.from_markup("[cyan]Construction du graphe de topologie...[/cyan]", justify="center")
            # Mettre à jour le bon élément dans le groupe
            if len(display_group.renderables) > 1:
                display_group.renderables[1] = Align.center(status_text)
            else:
                display_group.renderables.append(Align.center(status_text))
        if panel:
            live.update(panel)
        self._build_topology_graph()

        if display_group:
            status_text = Text.from_markup("[green]Chargement terminé avec succès.[/green]", justify="center")
            if len(display_group.renderables) > 1:
                display_group.renderables[1] = Align.center(status_text)
            if progress_bar in display_group.renderables:
                display_group.renderables.remove(progress_bar)
        if panel:
            live.update(panel)

        if manage_live:
            live.stop()

    def refresh_from_api(self, console, live=None, panel=None, display_group=None):
        """Met à jour le cache depuis l'API et détecte les changements."""
        
        # --- ÉTAPE 1: Sauvegarder l'état actuel ---
        old_data = {
            'Computer': {k: v for k, v in self.computers.items()},
            'NetworkEquipment': {k: v for k, v in self.network_equipments.items()},
            'PassiveDCEquipment': {k: v for k, v in self.passive_devices.items()},
            'Cable': {k: v for k, v in self.cables.items()},
            'Glpi\\Socket': {k: v for k, v in self.sockets.items()},
            'NetworkPort': {k: v for k, v in self.network_ports.items()},
        }
        
        # --- ÉTAPE 2: Recharger le cache ---
        # Cette partie est maintenant dans une méthode de chargement qui vide puis remplit
        self.load_from_api(console, live, panel, display_group)

        # --- ÉTAPE 3: Comparer l'ancien et le nouvel état ---
        self.changelog = [] # Réinitialiser le journal des changements
        new_data = {
            'Computer': self.computers,
            'NetworkEquipment': self.network_equipments,
            'PassiveDCEquipment': self.passive_devices,
            'Cable': self.cables,
            'Glpi\\Socket': self.sockets,
            'NetworkPort': self.network_ports,
        }

        for itemtype, old_items_dict in old_data.items():
            new_items_dict = new_data.get(itemtype, {})
            
            old_ids = set(old_items_dict.keys())
            new_ids = set(new_items_dict.keys())

            # Détecter les suppressions
            for removed_id in old_ids - new_ids:
                self.changelog.append({
                    'action': 'SUPPRESSION',
                    'type': itemtype,
                    'id': removed_id,
                    'name': getattr(old_items_dict[removed_id], 'name', 'N/A')
                })

            # Détecter les ajouts et les modifications
            for added_id in new_ids:
                if added_id not in old_ids:
                    # C'est un ajout
                    self.changelog.append({
                        'action': 'AJOUT',
                        'type': itemtype,
                        'id': added_id,
                        'name': getattr(new_items_dict[added_id], 'name', 'N/A')
                    })
                else:
                    # C'est un objet existant, vérifier s'il a été modifié
                    old_item = old_items_dict[added_id]
                    new_item = new_items_dict[added_id]
                    if getattr(old_item, 'date_mod', None) != getattr(new_item, 'date_mod', None):
                        # --- DÉBUT DE LA MODIFICATION ---
                        changed_fields = {}
                        # Comparer les attributs simples pour trouver les différences
                        for key, old_value in vars(old_item).items():
                            new_value = getattr(new_item, key, None)
                            # On ne compare que les types simples pour l'instant
                            if isinstance(old_value, (str, int, float)) and old_value != new_value:
                                changed_fields[key] = {'from': old_value, 'to': new_value}
                        
                        self.changelog.append({
                            'action': 'MODIFICATION',
                            'type': itemtype,
                            'id': added_id,
                            'name': getattr(new_item, 'name', 'N/A'),
                            'changes': changed_fields # On stocke les changements détaillés
                        })
                        # --- FIN DE LA MODIFICATION ---
        
        return len(self.changelog)

    def _build_topology_graph(self):
        # Dictionnaires globaux pour un accès rapide
        all_equipment = {**self.computers, **self.network_equipments, **self.passive_devices}
        name_to_id_map = {getattr(eq, 'name', '').lower(): eq_id for eq_id, eq in all_equipment.items()}

        # --- Étape 1: Initialisation des attributs sur tous les objets ---
        for equip in all_equipment.values():
            equip.ports = []
            equip.sockets = []
        for port in self.network_ports.values():
            port.parent = None
            port.socket = None
        for socket in self.sockets.values():
            socket.parent = None
            socket.port = None
            socket.connection = None

        # --- ÉTAPE 2: LIAISON PARENT-PORT & PARENT-SOCKET (LA CLÉ) ---
        # On parcourt les ports, qui connaissent leur parent ID
        for port in self.network_ports.values():
            parent_id = getattr(port, 'items_id', None)
            if parent_id in all_equipment:
                parent_equip = all_equipment[parent_id]
                port.parent = parent_equip
                parent_equip.ports.append(port)

        # On parcourt les sockets, qui connaissent aussi leur parent ID (parfois par nom)
        for socket in self.sockets.values():
            parent_id_or_name = getattr(socket, 'items_id', None)
            parent_equip = None
            if isinstance(parent_id_or_name, int):
                parent_equip = all_equipment.get(parent_id_or_name)
            elif isinstance(parent_id_or_name, str):
                parent_id = name_to_id_map.get(parent_id_or_name.lower())
                if parent_id:
                    parent_equip = all_equipment.get(parent_id)

            if parent_equip:
                socket.parent = parent_equip
                parent_equip.sockets.append(socket)
                # On remplit notre index ici
                if parent_equip.id not in self.equipment_to_sockets_map:
                    self.equipment_to_sockets_map[parent_equip.id] = []
                self.equipment_to_sockets_map[parent_equip.id].append(socket.id)

        # --- ÉTAPE 3: LIAISON PORT-SOCKET ---
        for socket in self.sockets.values():
            port_id = getattr(socket, 'networkports_id', None)
            if port_id and port_id in self.network_ports:
                network_port = self.network_ports[port_id]
                socket.port = network_port
                network_port.socket = socket

        # --- ÉTAPE 4: LIAISON CÂBLE-SOCKET ---
        for cable in self.cables.values():
            socket_ids = [int(link['href'].split('/')[-1]) for link in getattr(cable, 'links', []) if link.get('rel') == 'Glpi\\Socket']
            if len(socket_ids) == 2:
                socket_a = self.sockets.get(socket_ids[0])
                socket_b = self.sockets.get(socket_ids[1])
                if socket_a and socket_b:
                    socket_a.connection = {'via_cable': cable, 'to_socket': socket_b}
                    socket_b.connection = {'via_cable': cable, 'to_socket': socket_a}

    def get_sockets_for_item_id(self, item_id):
        return self.equipment_to_sockets_map.get(item_id, [])

    def _process_and_flatten_ports(self, item_details):
        flattened_ports = []
        raw_ports_data = item_details.get("_networkports", {})
        
        if not raw_ports_data:
            return flattened_ports

        for port_type, port_list in raw_ports_data.items():
            for port_data in port_list:
                # Créer un objet simple avec uniquement les clés qui nous intéressent
                port_obj = types.SimpleNamespace(
                    id=port_data.get('id'),
                    name=port_data.get('name'),
                    mac=port_data.get('mac'),
                    speed=port_data.get('speed')
                    # Ajoutez d'autres clés si nécessaire
                )
                flattened_ports.append(port_obj)
        
        return flattened_ports

    def _load_computers(self, progress, main_task_id, live, panel, display_group):
        status_text = Text.from_markup("[cyan]Chargement des ordinateurs...[/cyan]", justify="center")
        if len(display_group.renderables) > 1:
            display_group.renderables[1] = Align.center(status_text)
        else:
            display_group.renderables.append(Align.center(status_text))
        live.update(panel)
        id_list = self.api_client.list_items('Computer', item_range="0-9999", only_id=True)
        if not id_list:
            progress.advance(main_task_id)
            return
        sub_task = progress.add_task("Ordinateurs", total=len(id_list))
        for item_ref in id_list:
            item_id = item_ref.get('id')
            if item_id:
                details = self.api_client.get_item_details('Computer', item_id)
                if details:
                    details['itemtype'] = 'Computer'
                    item_obj = types.SimpleNamespace(**details)
                    item_obj.ports = self._process_and_flatten_ports(details)
                    self.computers[item_id] = item_obj
            progress.advance(sub_task)
        progress.remove_task(sub_task)
        progress.advance(main_task_id)

    def _load_network_equipments(self, progress, main_task_id, live, panel, display_group):
        status_text = Text.from_markup("[cyan]Chargement des équipements réseau...[/cyan]", justify="center")
        if len(display_group.renderables) > 1:
            display_group.renderables[1] = Align.center(status_text)
        else:
            display_group.renderables.append(Align.center(status_text))
        live.update(panel)
        id_list = self.api_client.list_items('NetworkEquipment', item_range="0-9999", only_id=True)
        if not id_list:
            progress.advance(main_task_id)
            return
        sub_task = progress.add_task("Équipements réseau", total=len(id_list))
        for item_ref in id_list:
            item_id = item_ref.get('id')
            if item_id:
                details = self.api_client.get_item_details('NetworkEquipment', item_id)
                if details:
                    details['itemtype'] = 'NetworkEquipment'
                    item_obj = types.SimpleNamespace(**details)
                    item_obj.ports = self._process_and_flatten_ports(details)
                    self.network_equipments[item_id] = item_obj
            progress.advance(sub_task)
        progress.remove_task(sub_task)
        progress.advance(main_task_id)

    def _load_passive_devices(self, progress, main_task_id, live, panel, display_group):
        status_text = Text.from_markup("[cyan]Chargement des équipements passifs...[/cyan]", justify="center")
        if len(display_group.renderables) > 1:
            display_group.renderables[1] = Align.center(status_text)
        else:
            display_group.renderables.append(Align.center(status_text))
        live.update(panel)
        id_list = self.api_client.list_items('PassiveDCEquipment', item_range="0-9999", only_id=True)
        if not id_list:
            progress.advance(main_task_id)
            return
        sub_task = progress.add_task("Équipements passifs", total=len(id_list))
        for item_ref in id_list:
            item_id = item_ref.get('id')
            if item_id:
                details = self.api_client.get_item_details('PassiveDCEquipment', item_id)
                if details:
                    details['itemtype'] = 'PassiveDCEquipment'
                    self.passive_devices[item_id] = types.SimpleNamespace(**details)
            progress.advance(sub_task)
        progress.remove_task(sub_task)
        progress.advance(main_task_id)

    def _load_cables(self, progress, main_task_id, live, panel, display_group):
        status_text = Text.from_markup("[cyan]Chargement des câbles...[/cyan]", justify="center")
        if len(display_group.renderables) > 1:
            display_group.renderables[1] = Align.center(status_text)
        else:
            display_group.renderables.append(Align.center(status_text))
        live.update(panel)
        id_list = self.api_client.list_items('Cable', item_range="0-9999", only_id=True)
        if not id_list:
            progress.advance(main_task_id)
            return
        sub_task = progress.add_task("Câbles", total=len(id_list))
        for item_ref in id_list:
            item_id = item_ref.get('id')
            if item_id:
                details = self.api_client.get_item_details('Cable', item_id)
                if details:
                    details['itemtype'] = 'Cable'
                    self.cables[item_id] = types.SimpleNamespace(**details)
            progress.advance(sub_task)
        progress.remove_task(sub_task)
        progress.advance(main_task_id)

    def _load_sockets(self, progress, main_task_id, live, panel, display_group):
        status_text = Text.from_markup("[cyan]Chargement des sockets...[/cyan]", justify="center")
        if len(display_group.renderables) > 1:
            display_group.renderables[1] = Align.center(status_text)
        else:
            display_group.renderables.append(Align.center(status_text))
        live.update(panel)
        id_list = self.api_client.list_items('Glpi\\Socket', item_range="0-9999", only_id=True)
        if not id_list:
            progress.advance(main_task_id)
            return
        sub_task = progress.add_task("Sockets", total=len(id_list))
        for item_ref in id_list:
            item_id = item_ref.get('id')
            if item_id:
                details = self.api_client.get_item_details('Glpi\\Socket', item_id)
                if details:
                    details['itemtype'] = 'Glpi\\Socket'
                    self.sockets[item_id] = types.SimpleNamespace(**details)
            progress.advance(sub_task)
        progress.remove_task(sub_task)
        progress.advance(main_task_id)

    def _load_network_ports(self, progress, main_task_id, live, panel, display_group):
        status_text = Text.from_markup("[cyan]Chargement des ports réseau...[/cyan]", justify="center")
        if len(display_group.renderables) > 1:
            display_group.renderables[1] = Align.center(status_text)
        else:
            display_group.renderables.append(Align.center(status_text))
        live.update(panel)
        id_list = self.api_client.list_items('NetworkPort', item_range="0-9999", only_id=True)
        if not id_list:
            progress.advance(main_task_id)
            return
        sub_task = progress.add_task("Ports réseau", total=len(id_list))
        for item_ref in id_list:
            item_id = item_ref.get('id')
            if item_id:
                details = self.api_client.get_item_details('NetworkPort', item_id)
                if details:
                    details['itemtype'] = 'NetworkPort'
                    self.network_ports[item_id] = types.SimpleNamespace(**details)
            progress.advance(sub_task)
        progress.remove_task(sub_task)
        progress.advance(main_task_id)

    def save_to_disk(self):
        """Sauvegarde l'état actuel du cache dans un fichier pickle."""
        try:
            cache_dir = os.path.dirname(self.cache_file)
            if not os.path.exists(cache_dir):
                os.makedirs(cache_dir)
            with open(self.cache_file, 'wb') as f:
                pickle.dump(self, f)
            # self.console.print("[dim]Cache sauvegardé sur le disque.[/dim]")
        except Exception as e:
            # self.console.print(f"[red]Erreur lors de la sauvegarde du cache : {e}[/red]")
            pass

    @classmethod
    def load_from_disk(cls, cache_file):
        """Charge une instance de TopologyCache depuis un fichier pickle."""
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'rb') as f:
                    return pickle.load(f)
            except Exception:
                # Si le fichier est corrompu, on retourne None
                return None
        return None