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
        # Créer un dictionnaire global de tous les équipements pour un accès facile
        all_equipment = {**self.computers, **self.network_equipments, **self.passive_devices}

        # --- Étape 1: Lier chaque Port/Socket à son parent Équipement ---
        # Un NetworkPort a un 'items_id' et 'itemtype' vers son parent
        for port in self.network_ports.values():
            parent_id = getattr(port, 'items_id', None)
            if parent_id in all_equipment:
                port.parent_item = all_equipment[parent_id]
                # Créer une liste de ports sur l'objet parent si elle n'existe pas
                if not hasattr(port.parent_item, 'networkports'):
                    port.parent_item.networkports = []
                port.parent_item.networkports.append(port)

        # Un Socket est lié à un NetworkPort par 'networkports_id'
        for socket in self.sockets.values():
            port_id = getattr(socket, 'networkports_id', None)
            if port_id in self.network_ports:
                socket.networkport = self.network_ports[port_id]
                # Lier en retour le socket au port
                self.network_ports[port_id].socket = socket

        # --- Étape 2: Lier les Sockets entre eux via les Câbles ---
        for cable in self.cables.values():
            socket_ids = []
            for link in getattr(cable, 'links', []):
                if link.get('rel') == 'Glpi\\Socket':
                    try:
                        socket_id = int(link['href'].split('/')[-1])
                        socket_ids.append(socket_id)
                    except (ValueError, IndexError):
                        continue
            
            if len(socket_ids) == 2:
                socket_a = self.sockets.get(socket_ids[0])
                socket_b = self.sockets.get(socket_ids[1])
                if socket_a and socket_b:
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
