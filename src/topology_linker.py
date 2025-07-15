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

    def find_socket_by_id(self, socket_id):
        """Trouve un objet socket par son ID."""
        return self.cache.sockets.get(socket_id)

    def find_connection_for_socket(self, start_socket):
        """
        Trouve le socket connecté à un autre via un câble.
        Retourne un dictionnaire {'via_cable': ..., 'other_socket': ...} ou None.
        """
        start_socket_id = getattr(start_socket, 'id', None)
        if not start_socket_id:
            return None

        for cable in self.cache.cables.values():
            socket_ids = []
            for link in getattr(cable, 'links', []):
                if link.get('rel') == 'Glpi\\Socket':
                    try:
                        socket_ids.append(int(link['href'].split('/')[-1]))
                    except (ValueError, IndexError):
                        continue
            
            if len(socket_ids) == 2 and start_socket_id in socket_ids:
                id1, id2 = socket_ids
                other_socket_id = id2 if id1 == start_socket_id else id1
                other_socket = self.cache.sockets.get(other_socket_id)
                
                if other_socket:
                    return {'via_cable': cable, 'other_socket': other_socket}
        
        return None
