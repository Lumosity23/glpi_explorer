from src.commands.base_command import BaseCommand
from rich.table import Table
from rich.panel import Panel
from rich.console import Console
from rich import box

class TraceCommand(BaseCommand):
    def __init__(self, cache, api_client, console):
        super().__init__(api_client, console)
        self.cache = cache
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

        start_item = self._find_item_in_cache(item_type, item_name)

        if not start_item:
            self._display_error(f"Item '{item_name}' of type '{item_type}' not found in cache.")
            return

        self._perform_trace(start_item)

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

    def _perform_trace(self, start_item):
        table = Table(title=f"Trace from {start_item.name}", box=box.MINIMAL)
        table.add_column("Step", style="cyan")
        table.add_column("Equipment")
        table.add_column("Socket Name")
        table.add_column("Connected Via")

        visited_sockets = set()
        current_socket = self._get_first_socket(start_item)
        step = 1

        while current_socket:
            if current_socket.id in visited_sockets:
                table.add_row(str(step), "Loop detected!", "", "")
                break
            
            visited_sockets.add(current_socket.id)
            
            parent_equipment = getattr(current_socket, 'parent_equipment', None)
            connection_info = "Cable" # Assuming cable connection for now

            table.add_row(
                str(step),
                parent_equipment.name if parent_equipment else "N/A",
                current_socket.name,
                connection_info
            )

            if not hasattr(current_socket, 'connected_to') or not current_socket.connected_to:
                table.add_row(str(step + 1), "End of connection", "", "")
                break

            next_socket = current_socket.connected_to
            
            # Handle passive equipment traversal
            next_equipment = getattr(next_socket, 'parent_equipment', None)
            if next_equipment and next_equipment.glpi_itemtype == 'PassiveDCEquipment':
                # This logic might need to be adjusted based on how passive devices are handled with sockets
                # For now, we just follow the direct connection.
                current_socket = next_socket
            else:
                current_socket = next_socket

            step += 1

        self.console.print(Panel(table, expand=False))

    def _get_first_socket(self, item):
        if hasattr(item, 'sockets') and item.sockets:
            return item.sockets[0]
        return None