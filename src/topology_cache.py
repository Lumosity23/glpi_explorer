from datetime import datetime
import pickle
import types
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.panel import Panel
from rich.console import Console, Group
from rich.text import Text
from rich.live import Live
from rich.align import Align
import os
from src.topology_linker import TopologyLinker

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
        # Re-créer le linker après la désérialisation
        from src.topology_linker import TopologyLinker
        self.linker = TopologyLinker(self)

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
        self._clear_data()
        self.console = console

        use_live_display = live is not None and panel is not None and display_group is not None

        progress_bar = None
        main_task = None
        if use_live_display:
            progress_bar = Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            )
            main_task = progress_bar.add_task("Chargement de la topologie...", total=6)
            display_group.renderables.append(progress_bar)
            live.update(panel)

        # --- Chargement des données ---
        self._load_computers(progress_bar, main_task, live, panel, display_group)
        self._load_network_equipments(progress_bar, main_task, live, panel, display_group)
        self._load_passive_devices(progress_bar, main_task, live, panel, display_group)
        self._load_cables(progress_bar, main_task, live, panel, display_group)
        self._load_sockets(progress_bar, main_task, live, panel, display_group)
        self._load_network_ports(progress_bar, main_task, live, panel, display_group)
        
        # --- Finalisation ---
        if use_live_display:
            status_text = Text.from_markup("[cyan]Construction du graphe de topologie...[/cyan]", justify="center")
            if len(display_group.renderables) > 1:
                for i, item in enumerate(display_group.renderables):
                    if isinstance(item, Align):
                        display_group.renderables[i] = Align.center(status_text)
                        break
                else:
                     display_group.renderables.insert(1, Align.center(status_text))
            else:
                display_group.renderables.append(Align.center(status_text))
            live.update(panel)

        self._build_topology_graph()

        if use_live_display:
            status_text = Text.from_markup("[green]Chargement terminé avec succès.[/green]", justify="center")
            if len(display_group.renderables) > 1:
                for i, item in enumerate(display_group.renderables):
                    if isinstance(item, Align):
                        display_group.renderables[i] = Align.center(status_text)
                        break
            if progress_bar in display_group.renderables:
                display_group.renderables.remove(progress_bar)
            live.update(panel)

    def get_all_data_copy(self):
        """Retourne une copie des dictionnaires de données principaux."""
        return {
            'Computer': {k: v for k, v in self.computers.items()},
            'NetworkEquipment': {k: v for k, v in self.network_equipments.items()},
            'PassiveDCEquipment': {k: v for k, v in self.passive_devices.items()},
            'Cable': {k: v for k, v in self.cables.items()},
            'Glpi\\Socket': {k: v for k, v in self.sockets.items()},
            'NetworkPort': {k: v for k, v in self.network_ports.items()},
        }

    def compare_and_log_changes(self, old_data):
        """Compare l'état actuel avec un état précédent et met à jour le changelog."""
        new_changes = []
        new_data = self.get_all_data_copy()

        all_item_types = set(old_data.keys()) | set(new_data.keys())

        for itemtype in all_item_types:
            old_items_dict = old_data.get(itemtype, {})
            new_items_dict = new_data.get(itemtype, {})
            
            old_ids = set(old_items_dict.keys())
            new_ids = set(new_items_dict.keys())

            # Détecter les suppressions
            for removed_id in old_ids - new_ids:
                item = old_items_dict[removed_id]
                new_changes.append({
                    'action': 'SUPPRESSION',
                    'type': itemtype, 'id': removed_id,
                    'name': getattr(item, 'name', 'N/A'),
                    'date_mod_glpi': getattr(item, 'date_mod', 'N/A')
                })

            # Détecter les ajouts et les modifications
            for item_id in new_ids:
                new_item = new_items_dict[item_id]
                if item_id not in old_ids:
                    new_changes.append({
                        'action': 'AJOUT',
                        'type': itemtype, 'id': item_id,
                        'name': getattr(new_item, 'name', 'N/A'),
                        'date_mod_glpi': getattr(new_item, 'date_mod', 'N/A')
                    })
                else:
                    old_item = old_items_dict[item_id]
                    if getattr(old_item, 'date_mod', None) != getattr(new_item, 'date_mod', None):
                        changed_fields = {}
                        for key, old_value in vars(old_item).items():
                            new_value = getattr(new_item, key, None)
                            if isinstance(old_value, (str, int, float)) and old_value != new_value:
                                changed_fields[key] = {'from': old_value, 'to': new_value}
                        
                        new_changes.append({
                            'action': 'MODIFICATION',
                            'type': itemtype, 'id': item_id,
                            'name': getattr(new_item, 'name', 'N/A'),
                            'date_mod_glpi': getattr(new_item, 'date_mod', 'N/A'),
                            'changes': changed_fields
                        })
        self.changelog.extend(new_changes)
        return len(new_changes)

    def _find_parent_in_cache(self, id_or_name, all_equipment, name_to_id_map):
        """Méthode d'aide unifiée pour trouver un parent."""
        if isinstance(id_or_name, int):
            return all_equipment.get(id_or_name)
        elif isinstance(id_or_name, str):
            parent_id = name_to_id_map.get(id_or_name.lower().strip())
            if parent_id:
                return all_equipment.get(parent_id)
        return None

    def _build_topology_graph(self):
        all_equipment = {**self.computers, **self.network_equipments, **self.passive_devices}
        name_to_id_map = {getattr(eq, 'name', '').lower().strip(): eq_id for eq_id, eq in all_equipment.items()}

        # --- Initialisation ---
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

        # --- ÉTAPE 1: Lier Ports et Sockets à leurs Parents ---
        for port in self.network_ports.values():
            parent_id_or_name = getattr(port, 'items_id', None)
            parent = self._find_parent_in_cache(parent_id_or_name, all_equipment, name_to_id_map)
            if parent:
                port.parent = parent
                parent.ports.append(port)

        for socket in self.sockets.values():
            parent_id_or_name = getattr(socket, 'items_id', None)
            parent = self._find_parent_in_cache(parent_id_or_name, all_equipment, name_to_id_map)
            if parent:
                socket.parent = parent
                parent.sockets.append(socket)
        
        # --- ÉTAPE 2: Lier Sockets et NetworkPorts ---
        for socket in self.sockets.values():
            port_id = getattr(socket, 'networkports_id', None)
            if port_id and port_id in self.network_ports:
                network_port = self.network_ports[port_id]
                socket.port = network_port
                network_port.socket = socket

        # --- ÉTAPE 3: Lier Sockets via Câbles ---
        for cable in self.cables.values():
            socket_ids = []
            for link in getattr(cable, 'links', []):
                if link.get('rel') == 'Glpi\\Socket':
                    try:
                        socket_ids.append(int(link['href'].split('/')[-1]))
                    except (ValueError, IndexError):
                        pass # Ignore malformed links
            if len(socket_ids) == 2:
                socket_a = self.sockets.get(socket_ids[0])
                socket_b = self.sockets.get(socket_ids[1])
                if socket_a and socket_b:
                    socket_a.connection = {'via_cable': cable, 'to_socket': socket_b}
                    socket_b.connection = {'via_cable': cable, 'to_socket': socket_a}

    def get_sockets_for_item_id(self, item_id):
        return self.equipment_to_sockets_map.get(item_id, [])

    

    def _load_computers(self, progress, main_task_id, live, panel, display_group):
        use_live_display = all(v is not None for v in [progress, main_task_id, live, panel, display_group])
        if use_live_display:
            status_text = Text.from_markup("[cyan]Chargement des ordinateurs...[/cyan]", justify="center")
            if len(display_group.renderables) > 1:
                display_group.renderables[1] = Align.center(status_text)
            else:
                display_group.renderables.append(Align.center(status_text))
            live.update(panel)
        
        id_list = self.api_client.list_items('Computer', item_range="0-9999", only_id=True)
        if not id_list:
            if use_live_display: progress.advance(main_task_id)
            return

        sub_task = progress.add_task("Ordinateurs", total=len(id_list)) if use_live_display else None
        for item_ref in id_list:
            item_id = item_ref.get('id')
            if item_id:
                details = self.api_client.get_item_details('Computer', item_id)
                if details:
                    details['itemtype'] = 'Computer'
                    item_obj = types.SimpleNamespace(**details)
                    self.computers[item_id] = item_obj
            if use_live_display: progress.advance(sub_task)
        if use_live_display:
            progress.remove_task(sub_task)
            progress.advance(main_task_id)

    def _load_network_equipments(self, progress, main_task_id, live, panel, display_group):
        use_live_display = all(v is not None for v in [progress, main_task_id, live, panel, display_group])
        if use_live_display:
            status_text = Text.from_markup("[cyan]Chargement des équipements réseau...[/cyan]", justify="center")
            if len(display_group.renderables) > 1:
                display_group.renderables[1] = Align.center(status_text)
            else:
                display_group.renderables.append(Align.center(status_text))
            live.update(panel)

        id_list = self.api_client.list_items('NetworkEquipment', item_range="0-9999", only_id=True)
        if not id_list:
            if use_live_display: progress.advance(main_task_id)
            return

        sub_task = progress.add_task("Équipements réseau", total=len(id_list)) if use_live_display else None
        for item_ref in id_list:
            item_id = item_ref.get('id')
            if item_id:
                details = self.api_client.get_item_details('NetworkEquipment', item_id)
                if details:
                    details['itemtype'] = 'NetworkEquipment'
                    item_obj = types.SimpleNamespace(**details)
                    self.network_equipments[item_id] = item_obj
            if use_live_display: progress.advance(sub_task)
        if use_live_display:
            progress.remove_task(sub_task)
            progress.advance(main_task_id)

    def _load_passive_devices(self, progress, main_task_id, live, panel, display_group):
        use_live_display = all(v is not None for v in [progress, main_task_id, live, panel, display_group])
        if use_live_display:
            status_text = Text.from_markup("[cyan]Chargement des équipements passifs...[/cyan]", justify="center")
            if len(display_group.renderables) > 1:
                display_group.renderables[1] = Align.center(status_text)
            else:
                display_group.renderables.append(Align.center(status_text))
            live.update(panel)

        id_list = self.api_client.list_items('PassiveDCEquipment', item_range="0-9999", only_id=True)
        if not id_list:
            if use_live_display: progress.advance(main_task_id)
            return

        sub_task = progress.add_task("Équipements passifs", total=len(id_list)) if use_live_display else None
        for item_ref in id_list:
            item_id = item_ref.get('id')
            if item_id:
                details = self.api_client.get_item_details('PassiveDCEquipment', item_id)
                if details:
                    details['itemtype'] = 'PassiveDCEquipment'
                    self.passive_devices[item_id] = types.SimpleNamespace(**details)
            if use_live_display: progress.advance(sub_task)
        if use_live_display:
            progress.remove_task(sub_task)
            progress.advance(main_task_id)

    def _load_cables(self, progress, main_task_id, live, panel, display_group):
        use_live_display = all(v is not None for v in [progress, main_task_id, live, panel, display_group])
        if use_live_display:
            status_text = Text.from_markup("[cyan]Chargement des câbles...[/cyan]", justify="center")
            if len(display_group.renderables) > 1:
                display_group.renderables[1] = Align.center(status_text)
            else:
                display_group.renderables.append(Align.center(status_text))
            live.update(panel)

        id_list = self.api_client.list_items('Cable', item_range="0-9999", only_id=True)
        if not id_list:
            if use_live_display: progress.advance(main_task_id)
            return

        sub_task = progress.add_task("Câbles", total=len(id_list)) if use_live_display else None
        for item_ref in id_list:
            item_id = item_ref.get('id')
            if item_id:
                details = self.api_client.get_item_details('Cable', item_id)
                if details:
                    details['itemtype'] = 'Cable'
                    self.cables[item_id] = types.SimpleNamespace(**details)
            if use_live_display: progress.advance(sub_task)
        if use_live_display:
            progress.remove_task(sub_task)
            progress.advance(main_task_id)

    def _load_sockets(self, progress, main_task_id, live, panel, display_group):
        use_live_display = all(v is not None for v in [progress, main_task_id, live, panel, display_group])
        if use_live_display:
            status_text = Text.from_markup("[cyan]Chargement des sockets...[/cyan]", justify="center")
            if len(display_group.renderables) > 1:
                display_group.renderables[1] = Align.center(status_text)
            else:
                display_group.renderables.append(Align.center(status_text))
            live.update(panel)

        id_list = self.api_client.list_items('Glpi\\Socket', item_range="0-9999", only_id=True)
        if not id_list:
            if use_live_display: progress.advance(main_task_id)
            return

        sub_task = progress.add_task("Sockets", total=len(id_list)) if use_live_display else None
        for item_ref in id_list:
            item_id = item_ref.get('id')
            if item_id:
                details = self.api_client.get_item_details('Glpi\\Socket', item_id)
                if details:
                    details['itemtype'] = 'Glpi\\Socket'
                    self.sockets[item_id] = types.SimpleNamespace(**details)
            if use_live_display: progress.advance(sub_task)
        if use_live_display:
            progress.remove_task(sub_task)
            progress.advance(main_task_id)

    def _load_network_ports(self, progress, main_task_id, live, panel, display_group):
        use_live_display = all(v is not None for v in [progress, main_task_id, live, panel, display_group])
        if use_live_display:
            status_text = Text.from_markup("[cyan]Chargement des ports réseau...[/cyan]", justify="center")
            if len(display_group.renderables) > 1:
                display_group.renderables[1] = Align.center(status_text)
            else:
                display_group.renderables.append(Align.center(status_text))
            live.update(panel)

        id_list = self.api_client.list_items('NetworkPort', item_range="0-9999", only_id=True)
        if not id_list:
            if use_live_display: progress.advance(main_task_id)
            return

        sub_task = progress.add_task("Ports réseau", total=len(id_list)) if use_live_display else None
        for item_ref in id_list:
            item_id = item_ref.get('id')
            if item_id:
                details = self.api_client.get_item_details('NetworkPort', item_id)
                if details:
                    details['itemtype'] = 'NetworkPort'
                    self.network_ports[item_id] = types.SimpleNamespace(**details)
            if use_live_display: progress.advance(sub_task)
        if use_live_display:
            progress.remove_task(sub_task)
            progress.advance(main_task_id)

    def save_to_disk(self):
        """Sauvegarde uniquement les données de topologie, pas l'état de la session."""
        data_to_save = {
            'computers': self.computers,
            'network_equipments': self.network_equipments,
            'passive_devices': self.passive_devices,
            'cables': self.cables,
            'sockets': self.sockets,
            'network_ports': self.network_ports
        }
        try:
            cache_dir = os.path.dirname(self.cache_file)
            if not os.path.exists(cache_dir):
                os.makedirs(cache_dir)
            with open(self.cache_file, 'wb') as f:
                pickle.dump(data_to_save, f)
        except Exception as e:
            pass

    @classmethod
    def load_from_disk(cls, cache_file, api_client, console):
        """Charge les données depuis le disque et retourne une NOUVELLE instance de cache."""
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'rb') as f:
                    saved_data = pickle.load(f)
                
                new_cache = cls(api_client, cache_file=cache_file)
                new_cache.console = console
                new_cache.computers = saved_data.get('computers', {})
                new_cache.network_equipments = saved_data.get('network_equipments', {})
                new_cache.passive_devices = saved_data.get('passive_devices', {})
                new_cache.cables = saved_data.get('cables', {})
                new_cache.sockets = saved_data.get('sockets', {})
                new_cache.network_ports = saved_data.get('network_ports', {})
                
                # Rebuild the topology graph after loading from disk
                new_cache._build_topology_graph()
                new_cache.linker = TopologyLinker(new_cache)
                return new_cache
            except Exception:
                return None
        return None