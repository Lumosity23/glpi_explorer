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
        """LA MÉTHODE CLÉ : Calcule le prochain saut, en gérant les passifs."""
        connection = self.find_connection_for_socket(current_socket)
        if not connection:
            return None # Fin de ligne

        next_socket_initial = connection['other_socket']
        next_parent = self.find_parent_for_socket(next_socket_initial)

        # Si on arrive sur un passif, on le "traverse"
        if next_parent and getattr(next_parent, 'itemtype', None) == 'PassiveDCEquipment':
            if " IN" in next_socket_initial.name.upper():
                out_port_name = next_socket_initial.name.upper().replace(" IN", " OUT")
                # Trouver le port OUT sur le même appareil
                sockets_of_passive = self.find_sockets_for_item(next_parent)
                out_socket = next((s for s in sockets_of_passive if s.name.upper() == out_port_name), None)
                
                if out_socket:
                    # On a traversé, le prochain hop part du port OUT
                    return {'type': 'traversal', 'from': next_socket_initial, 'to': out_socket, 'via': next_parent}
        
        # Est-ce qu'on a atterri sur un Hub ?
        # On l'identifie par son itemtype et le préfixe "HB" dans son nom.
        if next_parent and getattr(next_parent, 'itemtype', None) == 'NetworkEquipment' and getattr(next_parent, 'name', '').upper().startswith('HB'):
            
            # Trouver tous les sockets de ce hub
            sockets_of_hub = self.find_sockets_for_item(next_parent)
            if not sockets_of_hub: return next_socket_initial # Sécurité

            # Trouver le port OUT (celui avec le plus grand numéro de port)
            out_socket = None
            max_port_num = -1
            for s in sockets_of_hub:
                # Extraire le numéro du nom du port, ex: "HB eth port 5 OUT" -> 5
                try:
                    port_num = int(''.join(filter(str.isdigit, s.name)))
                    if port_num > max_port_num:
                        max_port_num = port_num
                        out_socket = s
                except ValueError:
                    continue

            # Si on est arrivé sur un port IN et qu'on a trouvé un port OUT
            if " IN" in next_socket_initial.name.upper() and out_socket:
                return {'type': 'traversal', 'from': next_socket_initial, 'to': out_socket, 'via': next_parent}
            
            # Si on est arrivé sur le port OUT, la trace s'arrête de ce côté
            if next_socket_initial == out_socket:
                return None
        
        # Dans tous les autres cas, on retourne la connexion physique
        return {'type': 'connection', 'socket': next_socket_initial, 'via': connection['via_cable']}