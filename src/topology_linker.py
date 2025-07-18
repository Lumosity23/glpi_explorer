# src/topology_linker.py

class TopologyLinker:
    def __init__(self, cache):
        self.cache = cache
        # Créer des maps inversées une seule fois pour la performance
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
        """Trouve l'équipement parent d'un socket."""
        parent_id_or_name = getattr(socket_obj, 'items_id', None)
        if isinstance(parent_id_or_name, int):
            return self._all_equipment.get(parent_id_or_name)
        elif isinstance(parent_id_or_name, str):
            return self._name_to_equip_map.get(parent_id_or_name.lower())
        return None

    def find_sockets_for_item(self, item_obj):
        """Trouve tous les sockets d'un équipement."""
        item_id = getattr(item_obj, 'id', None)
        item_name = getattr(item_obj, 'name', '').lower()
        if not (item_id or item_name): return []
        
        found_sockets = []
        for socket in self.cache.sockets.values():
            parent_id_or_name = getattr(socket, 'items_id', None)
            # Compare ID si possible, sinon compare nom
            if (isinstance(parent_id_or_name, int) and parent_id_or_name == item_id) or \
               (isinstance(parent_id_or_name, str) and parent_id_or_name.lower() == item_name):
                found_sockets.append(socket)
        return found_sockets

    def find_connection_for_socket(self, start_socket):
        """Trouve le câble et l'autre socket connecté."""
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
        """Trouve le port OUT d'un hub (numéro le plus élevé)."""
        sockets_on_hub = self.find_sockets_for_item(hub_equip)
        if not sockets_on_hub: return None
        
        out_socket = None
        max_num = -1
        for s in sockets_on_hub:
            try:
                # Extrait tous les nombres du nom et prend le dernier
                numbers = [int(c) for c in s.name if c.isdigit()]
                if not numbers: continue
                port_num = numbers[-1]
                if port_num > max_num:
                    max_num = port_num
                    out_socket = s
            except (ValueError, IndexError):
                if "OUT" in s.name.upper(): return s
        return out_socket

    def _get_passive_out_socket(self, passive_equip, in_socket):
        """Trouve le port OUT correspondant à un port IN sur un passif."""
        if " IN" not in in_socket.name.upper(): return None
        out_name = in_socket.name.upper().replace(" IN", " OUT")
        sockets_on_passive = self.find_sockets_for_item(passive_equip)
        return next((s for s in sockets_on_passive if s.name.upper() == out_name), None)