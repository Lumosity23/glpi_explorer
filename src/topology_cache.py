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
                item['itemtype'] = 'Cable'
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
        
        # Créer un dictionnaire de mapping nom -> objet pour une recherche rapide
        equipment_by_name = {getattr(eq, 'name', '').lower(): eq for eq in all_equipment.values()}

        for socket_obj in self.sockets.values():
            parent_id_or_name = getattr(socket_obj, 'items_id', None)
            
            parent_item = None
            
            # Tenter de trouver le parent par ID (si c'est un entier)
            if isinstance(parent_id_or_name, int) and parent_id_or_name in all_equipment:
                parent_item = all_equipment[parent_id_or_name]
            # Sinon, tenter de trouver par nom (si c'est une chaîne)
            elif isinstance(parent_id_or_name, str):
                parent_item = equipment_by_name.get(parent_id_or_name.lower())

            if parent_item:
                socket_obj.parent_item = parent_item
                socket_obj.parent_itemtype = getattr(parent_item, 'itemtype', None)
            else:
                socket_obj.parent_item = None
                socket_obj.parent_itemtype = None

        # Étape 2: Lier les sockets entre eux via les câbles, en utilisant les "links"
        for cable_obj in self.cables.values():
            socket_ids = []
            # Parcourir les liens du câble pour trouver les deux sockets
            for link in getattr(cable_obj, 'links', []):
                if link.get('rel') == 'Glpi\\Socket':
                    try:
                        # Extrait le dernier segment de l'URL, qui est l'ID
                        socket_id = int(link['href'].split('/')[-1])
                        socket_ids.append(socket_id)
                    except (ValueError, IndexError):
                        # Ignore les href mal formés
                        continue
            
            # Si nous avons trouvé exactement deux sockets, créons le lien
            if len(socket_ids) == 2:
                socket_a_id, socket_b_id = socket_ids
                
                if socket_a_id in self.sockets and socket_b_id in self.sockets:
                    socket_a = self.sockets[socket_a_id]
                    socket_b = self.sockets[socket_b_id]
                    
                    # Création du lien bidirectionnel
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
