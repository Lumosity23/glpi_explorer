import pickle
import types
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

class TopologyCache:
    def __init__(self, api_client, cache_file='topology_cache.pkl'):
        self.api_client = api_client
        self.cache_file = cache_file
        self.computers = {}
        self.network_equipments = {}
        self.passive_dc_equipments = {}
        self.cables = {}
        self.sockets = {}

    def load_from_api(self, console):
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
                self.computers[item['id']] = types.SimpleNamespace(**item)
            progress.advance(main_task)

            # Load NetworkEquipment
            progress.update(main_task, description="Chargement des Équipements Réseau...")
            network_equipments_data = self.api_client.list_items('NetworkEquipment', "0-9999")
            for item in network_equipments_data:
                self.network_equipments[item['id']] = types.SimpleNamespace(**item)
            progress.advance(main_task)

            # Load PassiveDCEquipment
            progress.update(main_task, description="Chargement des Équipements Passifs...")
            passive_equipments_data = self.api_client.list_items('PassiveDCEquipment', "0-9999")
            for item in passive_equipments_data:
                self.passive_dc_equipments[item['id']] = types.SimpleNamespace(**item)
            progress.advance(main_task)

            # Load Sockets
            progress.update(main_task, description="Chargement des Sockets...")
            self._load_sockets()
            progress.advance(main_task)

            # Load Cables
            progress.update(main_task, description="Chargement des Câbles...")
            cables_data = self.api_client.list_items('Cable', "0-9999")
            for item in cables_data:
                self.cables[item['id']] = types.SimpleNamespace(**item)
            progress.advance(main_task)

            # Link Topology
            progress.update(main_task, description="Création des liens réseau...")
            self._link_topology()
            progress.advance(main_task)

    def _load_sockets(self):
        sockets_data = self.api_client.list_items('Glpi\\Socket', "0-9999")
        for item in sockets_data:
            self.sockets[item['id']] = types.SimpleNamespace(**item)

    def _link_topology(self):
        all_devices = {
            'Computer': self.computers,
            'NetworkEquipment': self.network_equipments,
            'PassiveDCEquipment': self.passive_dc_equipments
        }

        for socket in self.sockets.values():
            itemtype = getattr(socket, 'itemtype', None)
            items_id = getattr(socket, 'items_id', None)
            if itemtype and items_id is not None and itemtype in all_devices:
                parent_device_dict = all_devices[itemtype]
                if items_id in parent_device_dict:
                    parent_device = parent_device_dict[items_id]
                    if not hasattr(parent_device, 'sockets'):
                        parent_device.sockets = []
                    parent_device.sockets.append(socket)
                    socket.parent_equipment = parent_device

        for cable in self.cables.values():
            socket_a_id = getattr(cable, 'sockets_id_endpoint_a', None)
            socket_b_id = getattr(cable, 'sockets_id_endpoint_b', None)

            if socket_a_id and socket_b_id and socket_a_id in self.sockets and socket_b_id in self.sockets:
                socket_a = self.sockets[socket_a_id]
                socket_b = self.sockets[socket_b_id]
                socket_a.connected_to = socket_b
                socket_b.connected_to = socket_a

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
