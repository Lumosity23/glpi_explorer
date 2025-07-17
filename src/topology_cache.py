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
            self._build_topology_graph()

            final_panel = Panel(
                Align.center(logo_text),
                title="Bienvenue dans GLPI Explorer",
                subtitle="v0.1"
            )
            live.update(final_panel)

    def _build_topology_graph(self):
        # Dictionnaires globaux pour un accès rapide
        all_equipment = {**self.computers, **self.network_equipments, **self.passive_devices}
        name_to_id_map = {getattr(eq, 'name', ''): eq_id for eq_id, eq in all_equipment.items()}

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
