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
            data['itemtype'] = item_type
            target_dict[data['id']] = types.SimpleNamespace(**data)
            progress.advance(task_id)

    def _link_topology(self):
        # Étape 1: Lier chaque socket à son équipement parent
        all_equipment = {**self.computers, **self.network_equipments, **self.passive_devices}

        # --- DÉBUT DU NOUVEAU BLOC DE CODE À AJOUTER ---

        # Étape 1: Lier chaque NetworkPort à son équipement parent
        for port in self.network_ports.values():
            parent_id = getattr(port, 'items_id', None)
            parent_itemtype = getattr(port, 'itemtype', None) # Assumant que l'itemtype est chargé
            
            # Utiliser le dictionnaire du bon type d'équipement
            parent_dict = None
            if parent_itemtype == 'Computer': parent_dict = self.computers
            elif parent_itemtype == 'NetworkEquipment': parent_dict = self.network_equipments
            elif parent_itemtype == 'PassiveDCEquipment': parent_dict = self.passive_devices
            
            if parent_dict and parent_id in parent_dict:
                parent_item = parent_dict[parent_id]
                port.parent_item = parent_item
                
                # Créer une liste de ports sur l'objet parent si elle n'existe pas
                if not hasattr(parent_item, 'networkports'):
                    parent_item.networkports = []
                parent_item.networkports.append(port)
        
        # --- FIN DU NOUVEAU BLOC DE CODE ---
        
        # Créer un dictionnaire de mapping nom -> objet pour une recherche rapide
        # .lower() pour une comparaison insensible à la casse
        equipment_by_name = {getattr(eq, 'name', '').lower(): eq for eq in all_equipment.values()}

        for socket_obj in self.sockets.values():
            parent_id_or_name = getattr(socket_obj, 'items_id', None)
            
            parent_item = None
            
            # Tenter de trouver le parent par ID (si c'est un entier)
            if isinstance(parent_id_or_name, int) and parent_id_or_name in all_equipment:
                parent_item = all_equipment.get(parent_id_or_name)
            # Sinon, tenter de trouver par nom (si c'est une chaîne)
            elif isinstance(parent_id_or_name, str):
                parent_item = equipment_by_name.get(parent_id_or_name.lower())

            if parent_item:
                socket_obj.parent_item = parent_item
                socket_obj.parent_itemtype = getattr(parent_item, 'itemtype', None)
            else:
                socket_obj.parent_item = None
                socket_obj.parent_itemtype = None

        # Étape 2: Lier les sockets entre eux via les câbles (cette partie reste inchangée)
        for cable_obj in self.cables.values():
            if 'links' in cable_obj.__dict__:
                for link in cable_obj.links:
                    item1_id = link.get('items1_id')
                    item2_id = link.get('items2_id')
                    
                    socket1 = self.sockets.get(item1_id)
                    socket2 = self.sockets.get(item2_id)
                    
                    if socket1 and socket2:
                        socket1.connected_to = socket2
                        socket2.connected_to = socket1
                        socket1.cable = cable_obj
                        socket2.cable = cable_obj

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
