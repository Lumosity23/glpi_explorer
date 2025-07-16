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

    def _find_parent_of_socket(self, socket_obj):
        """Trouve l'équipement parent d'un socket."""
        parent_id = getattr(socket_obj, 'items_id', None)
        parent_itemtype = getattr(socket_obj, 'itemtype', None)

        if not parent_id or not parent_itemtype:
            return None

        target_dict = None
        if parent_itemtype == 'Computer':
            target_dict = self.cache.computers
        elif parent_itemtype == 'NetworkEquipment':
            target_dict = self.cache.network_equipments
        elif parent_itemtype == 'PassiveDCEquipment':
            target_dict = self.cache.passive_devices
        
        if target_dict:
            return target_dict.get(parent_id)
        
        return None

    def get_next_hop(self, current_socket):
        """Orchestre la logique pour trouver le prochain saut dans la topologie."""
        connection = self.find_connection_for_socket(current_socket)
        if not connection:
            return None

        next_socket_physical = connection['other_socket']
        parent_equip = self._find_parent_of_socket(next_socket_physical)

        if not parent_equip:
            return next_socket_physical

        # Logique de traversée pour équipements passifs
        if getattr(parent_equip, 'itemtype', '') == 'PassiveDCEquipment':
            return self._handle_passive_traversal(next_socket_physical, parent_equip)

        # Logique de concentration pour les hubs
        if 'HB' in getattr(parent_equip, 'name', ''):
             return self._handle_hub_traversal(next_socket_physical, parent_equip)

        return next_socket_physical

    def _handle_passive_traversal(self, socket_in, parent_equip):
        """Gère la traversée d'un équipement passif."""
        socket_name = getattr(socket_in, 'name', '')
        if 'IN' in socket_name:
            out_name = socket_name.replace('IN', 'OUT')
            for socket in self.cache.sockets.values():
                if getattr(socket, 'items_id', None) == parent_equip.id and getattr(socket, 'name', '') == out_name:
                    return socket
        return socket_in

    def _handle_hub_traversal(self, socket_in, parent_equip):
        """Gère la logique d'un hub."""
        socket_name = getattr(socket_in, 'name', '')
        if 'IN' in socket_name:
            # Find the OUT port with the highest number
            out_port_name = ''
            highest_port_num = -1
            for socket in self.cache.sockets.values():
                if getattr(socket, 'items_id', None) == parent_equip.id:
                    if 'OUT' in getattr(socket, 'name', ''):
                        try:
                            port_num = int(socket.name.split(' ')[-1])
                            if port_num > highest_port_num:
                                highest_port_num = port_num
                                out_port_name = socket.name
                        except (ValueError, IndexError):
                            continue
            if out_port_name:
                for socket in self.cache.sockets.values():
                    if getattr(socket, 'items_id', None) == parent_equip.id and getattr(socket, 'name', '') == out_port_name:
                        return socket
        return None # Fin de trace si on arrive sur un port OUT

    def find_ports_for_item(self, item):
        """Trouve tous les ports réseau pour un équipement donné."""
        return getattr(item, 'ports', [])

    def find_socket_for_port(self, port):
        """Trouve le socket associé à un port réseau."""
        port_id = getattr(port, 'id', None)
        if not port_id:
            return None
        
        for socket in self.cache.sockets.values():
            if getattr(socket, 'networkports_id', None) == port_id:
                return socket
        return None

    def find_port_for_socket(self, socket):
        """Trouve le port réseau associé à un socket."""
        socket_id = getattr(socket, 'id', None)
        if not socket_id:
            return None

        for port in self.cache.network_ports.values():
            if getattr(port, 'sockets_id', None) == socket_id:
                return port
        return None

    def find_cable_between_sockets(self, socket_a, socket_b):
        """Trouve le câble qui connecte deux sockets."""
        socket_a_id = getattr(socket_a, 'id', None)
        socket_b_id = getattr(socket_b, 'id', None)
        if not socket_a_id or not socket_b_id:
            return None

        for cable in self.cache.cables.values():
            socket_ids = []
            for link in getattr(cable, 'links', []):
                if link.get('rel') == 'Glpi\\Socket':
                    try:
                        socket_ids.append(int(link['href'].split('/')[-1]))
                    except (ValueError, IndexError):
                        continue
            
            if len(socket_ids) == 2 and set(socket_ids) == {socket_a_id, socket_b_id}:
                return cable
        return None

    def build_path_from_item(self, start_item):
        path = []
        # On utilise les méthodes de recherche que nous avons conçues
        start_ports = self.find_ports_for_item(start_item)
        if not start_ports:
            return []
        
        current_port = start_ports[0] # On prend le premier port
        
        while current_port:
            current_socket = self.find_socket_for_port(current_port)
            if not current_socket: break
            
            connection = self.find_connection_for_socket(current_socket)
            if not connection:
                # C'est une fin de ligne
                # On pourrait ajouter une dernière étape "non connectée"
                break
                
            next_socket = connection['other_socket']
            
            # Logique pour la traversée des passifs (à ajouter ici)
            # ...
            
            # On stocke l'étape
            path.append({
                'start_equip_name': getattr(self._find_parent_of_socket(current_socket), 'name', 'N/A'),
                'start_port_name': current_port.name,
                'cable_name': connection['via_cable'].name,
                'end_equip_name': getattr(self._find_parent_of_socket(next_socket), 'name', 'N/A'),
                'end_port_name': getattr(self.find_port_for_socket(next_socket), 'name', next_socket.name),
            })
            
            # On passe à l'étape suivante
            current_port = self.find_port_for_socket(next_socket)

        return path