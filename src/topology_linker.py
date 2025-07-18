# src/topology_linker.py

class TopologyLinker:
    def __init__(self, cache):
        """
        Initialise le linker avec une référence au cache de topologie.
        
        Args:
            cache: Une instance de TopologyCache pleinement chargée.
        """
        self.cache = cache

    def find_item(self, itemtype, name):
        """Recherche un item par son nom et son type dans le cache."""
        target_dict = None
        if itemtype == 'Computer': target_dict = self.cache.computers
        elif itemtype == 'NetworkEquipment': target_dict = self.cache.network_equipments
        elif itemtype == 'PassiveDCEquipment': target_dict = self.cache.passive_devices
        # Ajoutez d'autres types si nécessaire
        
        if not target_dict:
            return None
        
        for item in target_dict.values():
            if getattr(item, 'name', '').lower() == name.lower():
                return item
        return None

    def find_sockets_for_item(self, item_obj):
        """Trouve tous les sockets d'un équipement en se basant sur le nom ou l'ID."""
        item_id = getattr(item_obj, 'id', None)
        item_name = getattr(item_obj, 'name', '').lower()
        found_sockets = []

        for socket in self.cache.sockets.values():
            parent_id_or_name = getattr(socket, 'items_id', None)
            if (isinstance(parent_id_or_name, int) and parent_id_or_name == item_id) or \
               (isinstance(parent_id_or_name, str) and parent_id_or_name.lower() == item_name):
                found_sockets.append(socket)
        return found_sockets

    def find_parent_for_socket(self, socket_obj):
        """Trouve l'équipement parent d'un socket."""
        all_equipment = {**self.cache.computers, **self.cache.network_equipments, **self.cache.passive_devices}
        equipment_by_name = {getattr(eq, 'name', ''): eq for eq in all_equipment.values()}
        
        parent_id_or_name = getattr(socket_obj, 'items_id', None)
        if isinstance(parent_id_or_name, int):
            return all_equipment.get(parent_id_or_name)
        elif isinstance(parent_id_or_name, str):
            return equipment_by_name.get(parent_id_or_name)
        return None

    def find_connection_for_socket(self, start_socket):
        """Trouve le câble et l'autre socket connecté."""
        start_socket_id = getattr(start_socket, 'id', None)
        if not start_socket_id: return None

        for cable in self.cache.cables.values():
            socket_ids = []
            for link in getattr(cable, 'links', []):
                if link.get('rel') == 'Glpi\\Socket':
                    try:
                        socket_id_from_link = int(link['href'].split('/')[-1])
                        socket_ids.append(socket_id_from_link)
                    except (ValueError, IndexError):
                        continue
            
            if len(socket_ids) == 2 and start_socket_id in socket_ids:
                id1, id2 = socket_ids
                other_socket_id = id2 if id1 == start_socket_id else id1
                other_socket = self.cache.sockets.get(other_socket_id)
                
                if other_socket:
                    return {'via_cable': cable, 'other_socket': other_socket}
        
        return None


    def get_next_hop(self, current_socket):
        parent = self.find_parent_for_socket(current_socket)
        
        # --- CAS 1: On est sur un équipement passif ---
        if parent and getattr(parent, 'itemtype', None) == 'PassiveDCEquipment':
            if " IN" in current_socket.name.upper():
                out_name = current_socket.name.upper().replace(" IN", " OUT")
                sockets_on_parent = self.find_sockets_for_item(parent)
                out_socket = next((s for s in sockets_on_parent if s.name.upper() == out_name), None)
                if out_socket:
                    return {'type': 'internal', 'socket': out_socket}

        # --- CAS 2: On est sur un Hub ---
        if parent and getattr(parent, 'itemtype', None) == 'NetworkEquipment' and getattr(parent, 'name', '').upper().startswith('HB'):
            sockets_on_hub = self.find_sockets_for_item(parent)
            # Trouver le port OUT (plus grand numéro)
            out_socket = max(sockets_on_hub, key=lambda s: int(''.join(filter(str.isdigit, s.name)) or 0))

            # Si on est sur un port IN, on saute au port OUT.
            if current_socket != out_socket:
                return {'type': 'internal', 'socket': out_socket}
            # Si on est déjà sur le port OUT, la trace continue normalement par le câble.

        # --- CAS 3: Connexion physique normale ---
        connection = self.find_connection_for_socket(current_socket)
        if connection:
            return {'type': 'connection', 'socket': connection['other_socket'], 'via': connection['via_cable']}
            
        # --- Fin de la ligne ---
        return None