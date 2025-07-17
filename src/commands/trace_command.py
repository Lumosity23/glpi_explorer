from .base_command import BaseCommand
from rich.panel import Panel
from rich.table import Table
from ..topology_linker import TopologyLinker

class TraceCommand(BaseCommand):
    def __init__(self, api_client, console, cache):
        super().__init__(api_client, console, cache)
        self.aliases = ["tr"]

    def get_help_message(self):
        return {
            "description": "Suit le chemin réseau d'un équipement de port en port.",
            "usage": "trace <type> <nom_objet>"
        }

    def execute(self, args):
        try:
            user_type_alias, item_name = args.split(maxsplit=1)
        except ValueError:
            self.console.print(Panel("Usage: trace <type> <nom_objet>", title="[red]Erreur[/red]"))
            return

        glpi_itemtype = self.TYPE_ALIASES.get(user_type_alias.lower())
        if not glpi_itemtype:
            self.console.print(Panel(f"Type inconnu : '{user_type_alias}'", title="[red]Erreur[/red]"))
            return

        linker = TopologyLinker(self.cache)
        start_item = linker.find_item(glpi_itemtype, item_name)

        if not start_item:
            self.console.print(Panel(f"Objet '{item_name}' non trouvé dans le cache.", title="[red]Erreur[/red]"))
            return

        start_item_id = getattr(start_item, 'id', None)
        
        # --- ÉTAPE 1: Trouver les sockets de départ via le nouvel index ---
        start_sockets = self.cache.get_sockets_for_item_id(start_item_id)
        
        if not start_sockets:
            self.console.print(Panel(f"Aucun socket physique trouvé pour {start_item.name} via l'index. Fin de la trace.", border_style="yellow"))
            return

        # Pour l'instant, on prend le premier socket trouvé.
        current_socket = start_sockets[0]
        
        # --- ÉTAPE 2: Initialisation et Boucle de traçage ---
        trace_table = Table(title=f"Trace depuis {start_item.name}", expand=True)
        trace_table.add_column("Étape")
        trace_table.add_column("Équipement")
        trace_table.add_column("Socket")
        trace_table.add_column("Câble")
        trace_table.add_column("Équipement Suivant")
        trace_table.add_column("Socket Suivant")

        visited_sockets = set()
        step = 1

        while current_socket and current_socket.id not in visited_sockets:
            visited_sockets.add(current_socket.id)
            
            parent = getattr(current_socket, 'parent_item', None)
            parent_name = getattr(parent, 'name', 'Parent Inconnu')

            next_socket = getattr(current_socket, 'connected_to', None)
            if next_socket:
                next_parent = getattr(next_socket, 'parent_item', None)
                next_parent_name = getattr(next_parent, 'name', 'Parent Inconnu')
                cable = linker.find_cable_between_sockets(current_socket, next_socket)
                cable_name = getattr(cable, 'name', 'N/A')
                trace_table.add_row(
                    str(step),
                    parent_name,
                    current_socket.name,
                    cable_name,
                    next_parent_name,
                    next_socket.name
                )
            else:
                trace_table.add_row(
                    str(step),
                    parent_name,
                    current_socket.name,
                    "N/A",
                    "N/A",
                    "N/A"
                )

            
            # Gérer la traversée des passifs (logique à venir)
            # ...
            
            current_socket = next_socket
            step += 1
            
        self.console.print(trace_table)
