import pickle
import types
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.panel import Panel
from rich.console import Console, Group
from rich.text import Text
from rich.live import Live
from rich.align import Align

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

    def load_from_api(self, console):
        self.console = console

        logo = """
         ██████╗ ██╗     ██████╗ ██╗      ███████╗██╗  ██╗██████╗ ██╗      ██████╗ ██████╗ ███████╗██████╗ 
        ██╔════╝ ██║     ██╔══██╗██║      ██╔════╝╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██╔══██╗██╔════╝██╔══██╗
        ██║  ███╗██║     ██████╔╝██║█████╗█████╗   ╚███╔╝ ██████╔╝██║     ██║   ██║██████╔╝█████╗  ██████╔╝
        ██║   ██║██║     ██╔═══╝ ██║╚════╝██╔══╝   ██╔██╗ ██╔═══╝ ██║     ██║   ██║██╔══██╗██╔══╝  ██╔══██╗
        ╚██████╔╝███████╗██║     ██║      ███████╗██╔╝ ██╗██║     ███████╗╚██████╔╝██║  ██║███████╗██║  ██║
         ╚═════╝ ╚══════╝╚═╝     ╚═╝      ╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
        """

        logo_text = Text(logo, justify="center", style="bold blue")

        progress_bar = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        )
        
        loading_group = Group(logo_text, progress_bar)
        panel = Panel(Align.center(loading_group))

        with Live(panel, console=console, redirect_stderr=False) as live:
            main_task = progress_bar.add_task("Chargement de la topologie...", total=6)

            self._load_computers(progress_bar, main_task)
            self._load_network_equipments(progress_bar, main_task)
            self._load_passive_devices(progress_bar, main_task)
            self._load_cables(progress_bar, main_task)
            self._load_sockets(progress_bar, main_task)
            self._load_network_ports(progress_bar, main_task)
            self._link_topology()

            final_panel = Panel(
                Align.center(logo_text),
                title="Bienvenue dans GLPI Explorer",
                subtitle="v0.1"
            )
            live.update(final_panel)

    def _link_topology(self):
        all_equipment = {**self.computers, **self.network_equipments, **self.passive_devices}
        equipment_by_name = {getattr(eq, 'name', '').lower(): eq for eq in all_equipment.values()}

        # --- ÉTAPE 1: Construire l'index Équipement -> Sockets ---
        for socket_id, socket in self.sockets.items():
            parent_id_or_name = getattr(socket, 'items_id', None)
            parent_item = None
            
            # Trouver le parent, que l'ID soit un entier ou un nom
            if isinstance(parent_id_or_name, int):
                parent_item = all_equipment.get(parent_id_or_name)
            elif isinstance(parent_id_or_name, str):
                parent_item = equipment_by_name.get(parent_id_or_name.lower())

            if parent_item:
                parent_id = getattr(parent_item, 'id', None)
                if parent_id:
                    if parent_id not in self.equipment_to_sockets_map:
                        self.equipment_to_sockets_map[parent_id] = []
                    self.equipment_to_sockets_map[parent_id].append(socket_id)
                # Lier le parent au socket pour une navigation facile
                socket.parent_item = parent_item
        
        # --- ÉTAPE 2: Lier les Sockets via les Câbles (ne change pas) ---
        for cable in self.cables.values():
            socket_ids = []
            for link in getattr(cable, 'links', []):
                if link.get('rel') == 'Glpi\Socket':
                    try:
                        link_socket_id = int(link['href'].split('/')[-1])
                        socket_ids.append(link_socket_id)
                    except (ValueError, IndexError):
                        continue
            
            if len(socket_ids) == 2:
                socket_a = self.sockets.get(socket_ids[0])
                socket_b = self.sockets.get(socket_ids[1])
                if socket_a and socket_b:
                    socket_a.connected_to = socket_b
                    socket_b.connected_to = socket_a

    def get_sockets_for_item_id(self, item_id):
        """Retourne une liste d'objets Socket pour un ID d'équipement donné."""
        socket_ids = self.equipment_to_sockets_map.get(item_id, [])
        return [self.sockets.get(sid) for sid in socket_ids if sid in self.sockets]

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

    def _load_computers(self, progress, main_task_id):
        progress.update(main_task_id, description="[cyan]Computers...")
        id_list = self.api_client.list_items('Computer', item_range="0-9999", only_id=True)
        if not id_list:
            progress.advance(main_task_id)
            return
        sub_task = progress.add_task("Chargement des détails...", total=len(id_list))
        for item_ref in id_list:
            item_id = item_ref.get('id')
            if item_id:
                details = self.api_client.get_item_details('Computer', item_id)
                if details:
                    item_obj = types.SimpleNamespace(**details)
                    item_obj.ports = self._process_and_flatten_ports(details)
                    self.computers[item_id] = item_obj
            progress.advance(sub_task)
        progress.remove_task(sub_task)
        progress.advance(main_task_id)

    def _load_network_equipments(self, progress, main_task_id):
        progress.update(main_task_id, description="[cyan]Network Equipments...")
        id_list = self.api_client.list_items('NetworkEquipment', item_range="0-9999", only_id=True)
        if not id_list:
            progress.advance(main_task_id)
            return
        sub_task = progress.add_task("Chargement des détails...", total=len(id_list))
        for item_ref in id_list:
            item_id = item_ref.get('id')
            if item_id:
                details = self.api_client.get_item_details('NetworkEquipment', item_id)
                if details:
                    item_obj = types.SimpleNamespace(**details)
                    item_obj.ports = self._process_and_flatten_ports(details)
                    self.network_equipments[item_id] = item_obj
            progress.advance(sub_task)
        progress.remove_task(sub_task)
        progress.advance(main_task_id)

    def _load_passive_devices(self, progress, main_task_id):
        progress.update(main_task_id, description="[cyan]Passive Devices...")
        id_list = self.api_client.list_items('PassiveDCEquipment', item_range="0-9999", only_id=True)
        if not id_list:
            progress.advance(main_task_id)
            return
        sub_task = progress.add_task("Chargement des détails...", total=len(id_list))
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

    def _load_cables(self, progress, main_task_id):
        progress.update(main_task_id, description="[cyan]Cables...")
        id_list = self.api_client.list_items('Cable', item_range="0-9999", only_id=True)
        if not id_list:
            progress.advance(main_task_id)
            return
        sub_task = progress.add_task("Chargement des détails...", total=len(id_list))
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

    def _load_sockets(self, progress, main_task_id):
        progress.update(main_task_id, description="[cyan]Sockets...")
        id_list = self.api_client.list_items('Glpi\\Socket', item_range="0-9999", only_id=True)
        if not id_list:
            progress.advance(main_task_id)
            return
        sub_task = progress.add_task("Chargement des détails...", total=len(id_list))
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

    def _load_network_ports(self, progress, main_task_id):
        progress.update(main_task_id, description="[cyan]Network Ports...")
        id_list = self.api_client.list_items('NetworkPort', item_range="0-9999", only_id=True)
        if not id_list:
            progress.advance(main_task_id)
            return
        sub_task = progress.add_task("Chargement des détails...", total=len(id_list))
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
        with open(self.cache_file, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load_from_disk(cache_file='topology_cache.pkl'):
        try:
            with open(cache_file, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return None
