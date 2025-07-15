from src.commands.base_command import BaseCommand
from rich.table import Table
from rich.panel import Panel
from rich.console import Console
from rich import box

class TraceCommand(BaseCommand):
    def __init__(self, api_client, console, cache):
        super().__init__(api_client, console, cache)
        self.name = "trace"
        self.description = "Trace a network path from a starting device through the topology cache."
        self.aliases = ["t"]

    def execute(self, args):
        if not args:
            self._display_error("Usage: trace <item_type> <item_name>")
            return

        parts = args.split(maxsplit=1)
        if len(parts) < 2:
            self._display_error("Usage: trace <item_type> <item_name>")
            return

        item_type_alias, item_name = parts
        item_type = self._get_item_type(item_type_alias)

        self.console.print(f"Starting trace for {item_name}")
        start_item = self._find_item_in_cache(item_type, item_name)

        if not start_item:
            self._display_error(f"Item '{item_name}' of type '{item_type}' not found in cache.")
            return

        self.console.print(f"Found start item: {start_item.name}")
        print(f"[DEBUG] ID of start_item: {id(start_item)}")
        if item_type == 'Computer':
            cached_item = self.cache.computers.get(start_item.id)
            if cached_item:
                print(f"[DEBUG] ID of cached_item (from self.cache.computers): {id(cached_item)}")
                print(f"[DEBUG] Are they the same object? {start_item is cached_item}")
                print(f"[DEBUG] networkports on cached_item: {getattr(cached_item, 'networkports', 'Attribute not found')}")
                print(f"[DEBUG] len(networkports on cached_item): {len(getattr(cached_item, 'networkports', []))}")
            else:
                print(f"[DEBUG] Cached item not found in self.cache.computers for ID {start_item.id}")
        self._perform_trace(start_item, item_type)

    def _find_item_in_cache(self, item_type, item_name):
        """Finds an item in the cache by its type and name."""
        target_cache_dict = None
        if item_type == 'Computer':
            target_cache_dict = self.cache.computers
        elif item_type == 'NetworkEquipment':
            target_cache_dict = self.cache.network_equipments
        elif item_type == 'PassiveDCEquipment':
            target_cache_dict = self.cache.passive_dc_equipments
        # Add other types as needed
        
        if target_cache_dict:
            for item in target_cache_dict.values():
                if item.name.lower() == item_name.lower():
                    return item
        return None

    def _perform_trace(self, start_item, start_itemtype):
        trace_table = Table(title=f"Trace depuis {start_item.name}", expand=True)
        trace_table.add_column("Étape", justify="right")
        trace_table.add_column("Équipement Parent")
        trace_table.add_column("Port Logique")
        trace_table.add_column("Socket Physique")
        trace_table.add_column("Connecté via (Câble)")

        # ÉTAPE 1: Trouver les ports de départ
        start_ports = self.cache.get_ports_for_item(start_item)
        if not start_ports:
            self.console.print(Panel("Aucun port réseau trouvé pour cet équipement.", border_style="yellow"))
            return
        
        current_port = start_ports[0] # On prend le premier
        current_socket = self.cache.get_socket_for_port(current_port)
        step = 1

        while current_socket:
            parent = self.cache.get_parent_for_socket(current_socket)
            parent_name = getattr(parent, 'name', 'Parent Inconnu')

            trace_table.add_row(str(step), parent_name, current_port.name, current_socket.name, "N/A")
            
            # ÉTAPE 2: Suivre la connexion
            next_socket = self.cache.get_connection_for_socket(current_socket)
            
            if not next_socket:
                break # Fin de la trace

            # Prépare l'itération suivante
            current_socket = next_socket
            # Ceci est une simplification. Il faudrait une méthode pour trouver le port d'un socket.
            # Pour l'instant, on suppose que la liaison inverse a été faite lors du chargement.
            current_port = getattr(current_socket, 'networkport', None)
            if not current_port:
                # Si le socket n'a pas de port logique (cas d'un patch panel), il faut le gérer
                # Pour l'instant on s'arrête
                break
            step += 1

        self.console.print(trace_table)