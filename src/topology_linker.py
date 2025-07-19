# src/topology_linker.py

class TopologyLinker:
    def __init__(self, cache):
        self.cache = cache
        # Créer des maps inversées une seule fois pour la performance
        
        # L'ancienne méthode de fusion écrasait les équipements ayant le même ID.
        # self._all_equipment = {**self.cache.computers, **self.cache.network_equipments, **self.cache.passive_devices}
        
        # CORRECTION: Construire la map de noms en itérant sur toutes les sources pour éviter les écrasements.
        self._name_to_equip_map = {}
        for eq_dict in [self.cache.computers, self.cache.network_equipments, self.cache.passive_devices]:
            for eq in eq_dict.values():
                name = getattr(eq, 'name', None)
                if name:
                    # Utilise le nom nettoyé comme clé
                    self._name_to_equip_map[name.lower().strip()] = eq

    def find_item(self, itemtype, name):
        # ... (cette méthode est correcte) ...
        target_dict = None
        if itemtype == 'Computer': target_dict = self.cache.computers
        elif itemtype == 'NetworkEquipment': target_dict = self.cache.network_equipments
        elif itemtype == 'PassiveDCEquipment': target_dict = self.cache.passive_devices
        if not target_dict: return None
        for item in target_dict.values():
            if getattr(item, 'name', '').lower() == name.lower():
                return item
        return None

    def find_parent_for_socket(self, socket_obj):
        """Trouve l'équipement parent d'un socket. CORRECTION FINALE."""
        parent_id_or_name = getattr(socket_obj, 'items_id', None)
        
        # Cas 1: L'ID est un entier, on cherche par ID dans toutes les sources pour éviter les collisions
        if isinstance(parent_id_or_name, int):
            return self.cache.computers.get(parent_id_or_name) or \
                   self.cache.network_equipments.get(parent_id_or_name) or \
                   self.cache.passive_devices.get(parent_id_or_name)
        
        # Cas 2: L'ID est un nom, on cherche par nom dans notre map corrigée
        elif isinstance(parent_id_or_name, str):
            return self._name_to_equip_map.get(parent_id_or_name.lower().strip())
        
        return None

    def find_sockets_for_item(self, item_obj):
        # ... (cette méthode est correcte) ...
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
        # ... (cette méthode est correcte) ...
        start_socket_id = getattr(start_socket, 'id', None)
        if not start_socket_id: return None
        for cable in self.cache.cables.values():
            socket_ids = [int(link['href'].split('/')[-1]) for link in getattr(cable, 'links', []) if link.get('rel') == 'Glpi\\Socket']
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
        """Calcule le prochain saut logique à partir d'un socket."""
        
        # 1. Tenter une traversée interne d'abord
        parent = self.find_parent_for_socket(current_socket)
        if not parent:
            return {'type': 'end', 'reason': 'Parent du socket actuel introuvable'}

        # CAS A: Équipement passif
        if getattr(parent, 'itemtype', None) == 'PassiveDCEquipment':
            if " IN" in current_socket.name.upper():
                out_socket = self._get_passive_out_socket(parent, current_socket)
                if out_socket:
                    return {'type': 'traversal', 'from': current_socket, 'to': out_socket, 'via': parent}
        
        # CAS B: Hub
        if getattr(parent, 'itemtype', None) == 'NetworkEquipment' and getattr(parent, 'name', '').upper().startswith('HB'):
            out_socket = self._get_hub_out_socket(parent)
            if out_socket and current_socket.id != out_socket.id:
                return {'type': 'traversal', 'from': current_socket, 'to': out_socket, 'via': parent}

        # 2. Si pas de traversée, chercher une connexion physique
        connection = self.find_connection_for_socket(current_socket)
        if connection:
            return {'type': 'connection', 'next_socket': connection['other_socket'], 'via_cable': connection['via_cable']}
            
        return {'type': 'end', 'reason': 'FIN DE LIGNE'}
