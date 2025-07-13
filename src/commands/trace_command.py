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
        trace_table.add_column("Socket")
        trace_table.add_column("Connecté via (Câble)")
        
        # Trouver les sockets de départ
        start_sockets = [s for s in self.cache.sockets.values() if getattr(s, 'items_id', None) == start_item.id]

        if not start_sockets:
            self.console.print(Panel(f"[yellow]Aucun socket physique trouvé pour {start_item.name}. Fin de la trace.[/yellow]", border_style="yellow"))
            return

        # Pour cette mission, on ne gère pas encore le choix interactif. On prend le premier.
        current_socket = start_sockets[0]
        visited_sockets = set()
        step = 1

        while current_socket and current_socket.id not in visited_sockets:
            visited_sockets.add(current_socket.id)
            parent_name = getattr(current_socket.parent_item, 'name', 'Parent Inconnu')
            cable_name = getattr(getattr(current_socket, 'via_cable', None), 'name', 'N/A')

            trace_table.add_row(
                str(step),
                parent_name,
                current_socket.name,
                cable_name
            )

            # Logique de traversée
            if hasattr(current_socket, 'connected_to'):
                next_socket = current_socket.connected_to
                
                # Gestion de la traversée des équipements passifs
                next_parent = getattr(next_socket, 'parent_item', None)
                if next_parent and getattr(next_parent, 'itemtype', None) == 'PassiveDCEquipment':
                    # Logique simplifiée : on suppose que le nom indique IN/OUT. Ex: "Port 1 IN", "Port 1 OUT"
                    if " IN" in next_socket.name.upper():
                        out_port_name = next_socket.name.upper().replace(" IN", " OUT")
                        # Trouver le port OUT correspondant sur le même équipement passif
                        found_out_port = False
                        for other_socket in self.cache.sockets.values():
                            if getattr(other_socket, 'parent_item', None) == next_parent and other_socket.name.upper() == out_port_name:
                                # On a trouvé le port de sortie, on affiche la traversée et on continue depuis là
                                trace_table.add_row(
                                    "",
                                    f"-> Traversée de {next_parent.name}",
                                    f"{next_socket.name} -> {other_socket.name}",
                                    "(Interne)"
                                )
                                current_socket = other_socket
                                found_out_port = True
                                break
                        if not found_out_port:
                            current_socket = None # Arrêt si pas de port OUT correspondant
                    else: # Si on arrive sur un port OUT, la logique est de continuer
                         current_socket = next_socket
                else: # Si ce n'est pas un passif, on continue normalement
                    current_socket = next_socket

            else: # Fin de la ligne
                current_socket = None
            
            step += 1
        
        self.console.print(trace_table)