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
        trace_table.add_column("Localisation")
        trace_table.add_column("Équipement")
        trace_table.add_column("Port / Traversée")
        
        visited_sockets = set()
        step = 1

        while current_socket and current_socket.id not in visited_sockets:
            visited_sockets.add(current_socket.id)
            
            parent = linker.find_parent_for_socket(current_socket)
            parent_name = getattr(parent, 'name', 'Parent Inconnu')
            parent_location = getattr(parent, 'locations_id', 'N/A')
            socket_name = getattr(current_socket, 'name', 'Socket Inconnu')

            hop = linker.get_next_hop(current_socket)
            
            # Afficher la ligne pour le point de départ du "hop"
            trace_table.add_row(str(step), parent_location, parent_name, socket_name)

            if not hop or hop['type'] == 'end':
                trace_table.add_row("", "", "", f"[bold yellow]--> {hop.get('reason', 'FIN DE TRACE')}[/bold yellow]")
                break

            next_socket_for_loop_check = hop.get('to_socket') or hop.get('next_socket')
            if next_socket_for_loop_check and next_socket_for_loop_check.id in visited_sockets:
                trace_table.add_row("", "", "", "[bold red]--> BOUCLE DÉTECTÉE, FIN DE TRACE[/bold red]")
                break
            
            if hop['type'] == 'connection':
                current_socket = hop['next_socket']
            elif hop['type'] == 'traversal':
                # Pour les traversées, on ajoute une ligne spéciale et on saute au port de sortie
                device_name = getattr(hop['via_device'], 'name', 'N/A')
                trace_table.add_row(
                    "", "", f"  [italic]-> Traversée de {device_name}[/italic]",
                    f"{hop['from_socket'].name} -> {hop['to_socket'].name}"
                )
                current_socket = hop['to_socket']
            
            step += 1
            
        self.console.print(trace_table)