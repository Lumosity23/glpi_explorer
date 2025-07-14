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
        
        # Trouver les ports de départ directement sur l'objet équipement
        start_ports = [p for p in self.cache.network_ports.values() if getattr(p, 'parent_item', None) == start_item]

        if not start_ports:
            self.console.print(Panel(f"Aucun port réseau trouvé pour {start_item.name}. Fin de la trace.", border_style="yellow"))
            return

        # Pour l'instant, on prend le premier port de l'équipement
        current_port = start_ports[0]
        # On récupère le socket physique associé à ce port logique
        current_socket = getattr(current_port, 'socket', None)
        
        # Handle case where current_port has no associated socket
        if not current_socket:
            self.console.print(Panel(f"Le port {current_port.name} de {start_item.name} n'a pas de socket physique associé. Fin de la trace.", border_style="yellow"))
            return
        
        # Handle case where current_port has no associated socket
        if not current_socket:
            self.console.print(Panel(f"Le port {current_port.name} de {start_item.name} n'a pas de socket physique associé. Fin de la trace.", border_style="yellow"))
            return
        
        visited_sockets = set()
        step = 1

        while current_socket and current_socket.id not in visited_sockets:
            visited_sockets.add(current_socket.id)
            
            # Récupérer le parent du port logique, qui est notre équipement
            parent_item = getattr(current_port, 'parent_item', None)
            parent_name = getattr(parent_item, 'name', 'Parent Inconnu')
            
            trace_table.add_row(
                str(step),
                parent_name,
                current_port.name, # Nom du port logique
                current_socket.name, # Nom du socket physique
                "N/A" # On gérera le câble plus tard
            )
            
            # On suit la connexion PHYSIQUE du socket
            if hasattr(current_socket, 'connected_to'):
                next_socket = current_socket.connected_to
                # On remonte au port logique suivant
                current_port = getattr(next_socket, 'networkport', None)
                current_socket = next_socket
            else:
                break # Fin de la trace
            
            step += 1
            
        self.console.print(trace_table)