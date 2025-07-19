# src/topology_linker.py

class TopologyLinker:
    def __init__(self, cache):
        self.cache = cache
        self._all_equipment = {**self.cache.computers, **self.cache.network_equipments, **self.cache.passive_devices}
        self._name_to_equip_map = {getattr(eq, 'name', '').lower(): eq for eq in self._all_equipment.values()}

    def find_item(self, itemtype, name):
        """Recherche un item par son nom et son type dans le cache. LOGIQUE FIABLE."""
        target_dict = None
        if itemtype == 'Computer': target_dict = self.cache.computers
        elif itemtype == 'NetworkEquipment': target_dict = self.cache.network_equipments
        elif itemtype == 'PassiveDCEquipment': target_dict = self.cache.passive_devices
        # ... (vous pouvez ajouter d'autres types ici si nécessaire) ...
        
        if not target_dict:
            return None
        
        for item in target_dict.values():
            if getattr(item, 'name', '').lower() == name.lower():
                return item
        return None
        
    def find_parent_for_socket(self, socket_obj):
        """Trouve l'équipement parent d'un socket en se basant sur l'itemtype et l'id."""
        parent_itemtype = getattr(socket_obj, 'itemtype', None)
        parent_id = getattr(socket_obj, 'items_id', None)

        if not all([parent_itemtype, parent_id]):
            return None

        # Détermine dans quel dictionnaire du cache chercher
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

    def find_sockets_for_item(self, item_obj):
        """Trouve tous les sockets d'un équipement."""
        item_id = getattr(item_obj, 'id', None)
        item_name = getattr(item_obj, 'name', '').lower()
        if not (item_id or item_name): return []
        
        found_sockets = []
        for socket in self.cache.sockets.values():
            parent_id_or_name = getattr(socket, 'items_id', None)
            if (isinstance(parent_id_or_name, int) and parent_id_or_name == item_id) or \
               (isinstance(parent_id_or_name, str) and parent_id_or_name.lower() == item_name):
                found_sockets.append(socket)
        return found_sockets

    def find_connection_for_socket(self, start_socket):
        """Trouve le câble et l'autre socket connecté."""
        start_socket_id = getattr(start_socket, 'id', None)
        if not start_socket_id: return None

        for cable in self.cache.cables.values():
            # Correction pour gérer les cas où 'links' n'existe pas ou est None
            links = getattr(cable, 'links', [])
            if not links: continue
            
            socket_ids = []
            for link in links:
                if link.get('rel') == 'Glpi\\Socket':
                    try:
                        socket_ids.append(int(link['href'].split('/')[-1]))
                    except (ValueError, IndexError):
                        continue # Ignorer les href mal formés

            if len(socket_ids) == 2 and start_socket_id in socket_ids:
                other_id = socket_ids[0] if socket_ids[1] == start_socket_id else socket_ids[1]
                other_socket = self.cache.sockets.get(other_id)
                if other_socket:
                    return {'via_cable': cable, 'other_socket': other_socket}
        return None

    def _get_hub_out_socket(self, hub_equip):
        """Trouve le port OUT d'un hub (nommé 'OUT' ou numéro le plus élevé)."""
        sockets_on_hub = self.find_sockets_for_item(hub_equip)
        if not sockets_on_hub: return None
        
        out_socket = None
        max_num = -1

        # Priorité 1: Chercher un port nommé "OUT"
        for s in sockets_on_hub:
            if "OUT" in s.name.upper():
                return s

        # Priorité 2: Chercher le port avec le numéro le plus élevé
        for s in sockets_on_hub:
            try:
                # Extrait le dernier nombre trouvé dans le nom du port
                numbers = [int(part) for part in s.name.replace("-", " ").split() if part.isdigit()]
                if not numbers: continue
                port_num = numbers[-1]
                if port_num > max_num:
                    max_num = port_num
                    out_socket = s
            except (ValueError, IndexError):
                continue
        return out_socket

    def _get_passive_out_socket(self, passive_equip, in_socket):
        """Trouve le port OUT correspondant à un port IN sur un passif."""
        # Logique simple basée sur le remplacement de "IN" par "OUT"
        if "IN" not in in_socket.name.upper(): return None
        
        # Gère des variations comme "Port 1 IN" -> "Port 1 OUT"
        # ou "IN 1" -> "OUT 1"
        out_name = in_socket.name.upper().replace("IN", "OUT")
        
        sockets_on_passive = self.find_sockets_for_item(passive_equip)
        return next((s for s in sockets_on_passive if s.name.upper() == out_name), None)

    def get_next_hop(self, current_socket):
        """
        Calcule le prochain saut dans la topologie à partir d'un socket donné.
        La logique est priorisée :
        1. Traversée d'équipement (Hub, Passif)
        2. Connexion par câble
        """
        parent_equip = self.find_parent_for_socket(current_socket)
        if not parent_equip:
            return {'type': 'end', 'reason': 'Socket orphelin'}

        itemtype = getattr(parent_equip, 'itemtype', None)

        # --- Logique de Traversée ---
        # Si on est sur un équipement qui doit être traversé, on le fait en priorité.
        
        # 1a. Traversée de Hub
        # Si on arrive sur un hub, on doit en ressortir par le port de sortie (uplink)
        if itemtype == 'NetworkEquipment' and 'hub' in getattr(parent_equip, 'name', '').lower():
            out_socket = self._get_hub_out_socket(parent_equip)
            # On vérifie qu'on n'est pas déjà sur le port de sortie pour éviter une boucle
            if out_socket and out_socket.id != current_socket.id:
                return {
                    'type': 'traversal',
                    'traversed_item': parent_equip,
                    'from_socket': current_socket,
                    'to_socket': out_socket
                }
            # Si on est déjà sur le port de sortie, on ne traverse pas, on cherche la connexion.
            # La logique continue plus bas.

        # 1b. Traversée d'équipement passif (ex: Patch Panel)
        # Si on arrive sur un port IN, on cherche le port OUT correspondant
        if itemtype == 'PassiveDCEquipment':
            out_socket = self._get_passive_out_socket(parent_equip, current_socket)
            if out_socket:
                return {
                    'type': 'traversal',
                    'traversed_item': parent_equip,
                    'from_socket': current_socket,
                    'to_socket': out_socket
                }
            # Si on est sur un port OUT, on ne traverse pas, on cherche la connexion.
            # La logique continue plus bas.

        # --- Logique de Connexion ---
        # Si aucune logique de traversée ne s'est appliquée, on cherche un câble.
        connection = self.find_connection_for_socket(current_socket)
        if connection:
            return {
                'type': 'connection',
                'via_cable': connection['via_cable'],
                'next_socket': connection['other_socket']
            }

        # --- Fin de Trace ---
        # Si on n'a trouvé ni traversée ni connexion, c'est la fin.
        return {'type': 'end', 'reason': 'Fin de ligne (pas de connexion ou de logique de traversée applicable)'}
