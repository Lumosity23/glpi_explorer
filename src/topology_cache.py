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
            progress.update(main_task, description="Chargement des Sockets Physiques...")
            self._load_sockets(progress, progress.add_task("Sockets...", total=1)) # Ajout
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

    def _load_sockets(self, progress, task_id):
        sockets_data = self.api_client.list_items('Glpi\Socket', "0-9999")
        progress.update(task_id, total=len(sockets_data))
        for data in sockets_data:
            self.sockets[data['id']] = types.SimpleNamespace(**data)
            progress.advance(task_id)

    def _link_topology(self):
        # Étape 1: Lier chaque socket à son équipement parent
        all_equipment = {**self.computers, **self.network_equipments, **self.passive_dc_equipments}
        for socket_obj in self.sockets.values():
            parent_id = getattr(socket_obj, 'items_id', None)
            if parent_id in all_equipment:
                socket_obj.parent_item = all_equipment[parent_id]
            else:
                socket_obj.parent_item = None

        # Étape 2: Lier les sockets entre eux via les câbles
        for cable_obj in self.cables.values():
            socket_a_id = getattr(cable_obj, 'sockets_id_endpoint_a', None)
            socket_b_id = getattr(cable_obj, 'sockets_id_endpoint_b', None)

            if socket_a_id in self.sockets and socket_b_id in self.sockets:
                socket_a = self.sockets[socket_a_id]
                socket_b = self.sockets[socket_b_id]
                
                socket_a.connected_to = socket_b
                socket_a.via_cable = cable_obj
                
                socket_b.connected_to = socket_a
                socket_b.via_cable = cable_obj

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
