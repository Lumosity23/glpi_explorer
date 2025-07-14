import pickle
import types
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

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

    def load_from_api(self, console):
        self.console = console
        progress_columns = [
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        ]
        with Progress(*progress_columns, console=console) as progress:
            main_task = progress.add_task("Chargement de la topologie...", total=7)

            # Load Computers
            progress.update(main_task, description="Chargement des Ordinateurs...")
            computers_data = self.api_client.list_items('Computer', "0-9999")
            for item in computers_data:
                item['itemtype'] = 'Computer'
                self.computers[item['id']] = types.SimpleNamespace(**item)
            progress.advance(main_task)

            # Load NetworkEquipment
            progress.update(main_task, description="Chargement des Équipements Réseau...")
            network_equipments_data = self.api_client.list_items('NetworkEquipment', "0-9999")
            for item in network_equipments_data:
                item['itemtype'] = 'NetworkEquipment'
                self.network_equipments[item['id']] = types.SimpleNamespace(**item)
            progress.advance(main_task)

            # Load PassiveDCEquipment
            progress.update(main_task, description="Chargement des Équipements Passifs...")
            passive_equipments_data = self.api_client.list_items('PassiveDCEquipment', "0-9999")
            for item in passive_equipments_data:
                item['itemtype'] = 'PassiveDCEquipment'
                self.passive_devices[item['id']] = types.SimpleNamespace(**item)
            progress.advance(main_task)

            # Load Sockets
            progress.update(main_task, description="Chargement des Sockets Physiques...")
            self._load_items('Glpi\\Socket', self.sockets, progress, progress.add_task("Sockets...", total=1))
            progress.advance(main_task)

            # Load Cables
            progress.update(main_task, description="Chargement des Câbles...")
            self._load_items('Cable', self.cables, progress, progress.add_task("Cables...", total=1))
            progress.advance(main_task)

            # Load NetworkPorts
            progress.update(main_task, description="Chargement des Ports Réseau...")
            self._load_items('NetworkPort', self.network_ports, progress, progress.add_task("NetworkPorts...", total=1))
            progress.advance(main_task)

            # Link Topology
            progress.update(main_task, description="Création des liens réseau...")
            self._link_topology()
            progress.advance(main_task)

    def _load_items(self, item_type, target_dict, progress, task_id):
        items_data = self.api_client.list_items(item_type, "0-9999")
        progress.update(task_id, total=len(items_data))
        for data in items_data:
            target_dict[data['id']] = types.SimpleNamespace(**data)
            progress.advance(task_id)

    def _link_topology(self):
        def _link_topology():        for port in self.network_ports.values():            parent_id_or_name = getattr(port, 'items_id', None)                        parent_item = None                        if isinstance(parent_id_or_name, int):                if parent_id_or_name in self.computers:                    parent_item = self.computers[parent_id_or_name]                elif parent_id_or_name in self.network_equipments:                    parent_item = self.network_equipments[parent_id_or_name]                elif parent_id_or_name in self.passive_devices:                    parent_item = self.passive_devices[parent_id_or_name]            elif isinstance(parent_id_or_name, str):                for comp_id, comp_obj in self.computers.items():                    if getattr(comp_obj, 'name', '').lower() == parent_id_or_name.lower():                        parent_item = comp_obj                        break                if not parent_item:                    for net_eq_id, net_eq_obj in self.network_equipments.items():                        if getattr(net_eq_obj, 'name', '').lower() == parent_id_or_name.lower():                            parent_item = net_eq_obj                            break                if not parent_item:                    for pass_dev_id, pass_dev_obj in self.passive_devices.items():                        if getattr(pass_dev_obj, 'name', '').lower() == parent_id_or_name.lower():                            parent_item = pass_dev_obj                            break            if parent_item:                port.parent_item = parent_item                if not hasattr(parent_item, 'networkports'):                    parent_item.networkports = []                parent_item.networkports.append(port)        for socket in self.sockets.values():            port_id = getattr(socket, 'networkports_id', None)            if port_id in self.network_ports:                socket.networkport = self.network_ports[port_id]                self.network_ports[port_id].socket = socket        for cable in self.cables.values():            socket_ids = []            for link in getattr(cable, 'links', []):                if link.get('rel') == 'Glpi\Socket':                    try:                        socket_id = int(link['href'].split('/')[-1])                        socket_ids.append(socket_id)                    except (ValueError, IndexError):                        continue                        if len(socket_ids) == 2:                socket_a = self.sockets.get(socket_ids[0])                socket_b = self.sockets.get(socket_ids[1])                if socket_a and socket_b:                    socket_a.connected_to = socket_b                    socket_b.connected_to = socket_a

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
