# src/commands/trace_command.py
from .base_command import BaseCommand
from ..topology_linker import TopologyLinker
from rich.panel import Panel
from rich.table import Table

class TraceCommand(BaseCommand):
    def __init__(self, api_client, console, cache):
        super().__init__(api_client, console, cache)
        self.aliases = ["tr"]

    def get_help_message(self):
        return { "description": "Suit le chemin réseau d'un équipement.", "usage": "trace <type> <nom_objet>" }

    def execute(self, args):
        try:
            user_type_alias, item_name = args.split(maxsplit=1)
        except ValueError:
            self.console.print(Panel("Usage: trace <type> <nom_objet>", title="[red]Erreur[/red]"))
            return
        
        linker = TopologyLinker(self.cache)
        itemtype = self.TYPE_ALIASES.get(user_type_alias.lower())
        start_item = linker.find_item(itemtype, item_name)
        if not start_item:
            self.console.print(Panel(f"Objet '{item_name}' non trouvé.", title="[red]Erreur[/red]"))
            return

        start_sockets = linker.find_sockets_for_item(start_item)
        if not start_sockets:
            self.console.print(Panel(f"Aucun socket trouvé pour {start_item.name}.", border_style="yellow"))
            return

        current_socket = start_sockets[0]
        
        trace_table = Table(title=f"Trace depuis {start_item.name}", expand=True)
        trace_table.add_column("Étape", justify="right")
        trace_table.add_column("Équipement")
        trace_table.add_column("Port / Traversée")
        trace_table.add_column("Via")
        
        visited_sockets = set()
        step = 1

        while current_socket and current_socket.id not in visited_sockets:
            visited_sockets.add(current_socket.id)
            parent = linker.find_parent_for_socket(current_socket)

            # On affiche la ligne pour le point actuel
            trace_table.add_row(
                str(step),
                getattr(parent, 'name', 'N/A'),
                current_socket.name,
                "..." # Placeholder
            )

            hop = linker.get_next_hop(current_socket)
            
            if not hop or hop['type'] == 'end':
                trace_table.rows[-1].cells[3] = "[bold yellow]DESTINATION FINALE[/bold yellow]"
                break
            
            if hop['type'] == 'connection':
                next_socket = hop['next_socket']
                next_parent = linker.find_parent_for_socket(next_socket)
                trace_table.rows[-1].cells[3] = f"[green]{getattr(hop['via_cable'], 'name', 'N/A')}[/green] -> [cyan]{getattr(next_parent, 'name', 'N/A')}[/cyan]"
                current_socket = next_socket
            
            elif hop['type'] == 'traversal':
                trace_table.rows[-1].cells[3] = f"([italic blue]Interne à {getattr(hop['via_device'], 'name', 'N/A')}[/italic blue])"
                current_socket = hop['to_socket']
            
            step += 1
        
        self.console.print(trace_table)