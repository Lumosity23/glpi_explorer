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
            main_task = progress.add_task("Chargement de la topologie...", total=6)

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

    def _load_items(self, item_type, target_dict, progress, task_id):
        items_data = self.api_client.list_items(item_type, "0-9999")
        progress.update(task_id, total=len(items_data))
        for data in items_data:
            data['itemtype'] = item_type
            target_dict[data['id']] = types.SimpleNamespace(**data)
            progress.advance(task_id)

    def get_ports_for_item(self, parent_item):
        """Recherche et retourne tous les NetworkPorts appartenant à un équipement parent."""
        found_ports = []
        parent_id = getattr(parent_item, 'id', None)
        parent_name = getattr(parent_item, 'name', '').lower()

        if not parent_id:
            return []

        for port in self.network_ports.values():
            port_parent_id_or_name = getattr(port, 'items_id', None)
            
            # Gère le cas où l'API retourne un ID numérique
            if isinstance(port_parent_id_or_name, int) and port_parent_id_or_name == parent_id:
                found_ports.append(port)
            # Gère le cas où l'API retourne un nom
            elif isinstance(port_parent_id_or_name, str) and port_parent_id_or_name.lower() == parent_name:
                found_ports.append(port)
        
        return found_ports

    def get_socket_for_port(self, network_port):
        """Trouve le Socket physique correspondant à un NetworkPort logique."""
        port_id = getattr(network_port, 'id', None)
        if not port_id:
            return None
            
        for socket in self.sockets.values():
            if getattr(socket, 'networkports_id', None) == port_id:
                return socket
        return None

    def get_connection_for_socket(self, socket):
        """Trouve le socket connecté à un autre via un câble."""
        socket_id = getattr(socket, 'id', None)
        if not socket_id:
            return None

        for cable in self.cables.values():
            socket_ids = []
            for link in getattr(cable, 'links', []):
                if link.get('rel') == 'Glpi\\Socket':
                    try:
                        link_socket_id = int(link['href'].split('/')[-1])
                        socket_ids.append(link_socket_id)
                    except (ValueError, IndexError):
                        continue
            
            if len(socket_ids) == 2:
                if socket_ids[0] == socket_id:
                    return self.sockets.get(socket_ids[1])
                elif socket_ids[1] == socket_id:
                    return self.sockets.get(socket_ids[0])
        return None

    def get_parent_for_socket(self, socket):
        """Trouve l'équipement parent d'un socket."""
        # Logique de la Mission 10.5
        all_equipment = {**self.computers, **self.network_equipments, **self.passive_devices}
        equipment_by_name = {getattr(eq, 'name', '').lower(): eq for eq in all_equipment.values()}
        
        parent_id_or_name = getattr(socket, 'items_id', None)
        
        if isinstance(parent_id_or_name, int) and parent_id_or_name in all_equipment:
            return all_equipment.get(parent_id_or_name)
        elif isinstance(parent_id_or_name, str):
            return equipment_by_name.get(parent_id_or_name.lower())
        return None

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