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

        start_sockets = linker.find_sockets_for_item(start_item)
        if not start_sockets:
            self.console.print(Panel(f"Aucun socket trouvé pour {start_item.name} dans le cache.", border_style="yellow"))
            return

        current_socket = start_sockets[0]
        
        trace_table = Table(title=f"Trace depuis {start_item.name}", expand=True)
        trace_table.add_column("Étape", justify="right")
        trace_table.add_column("Équipement")
        trace_table.add_column("Port")
        trace_table.add_column("Via (Câble)")
        
        visited_sockets = set()
        step = 1

        while current_socket and current_socket.id not in visited_sockets:
            visited_sockets.add(current_socket.id)
            
            parent = linker.find_parent_for_socket(current_socket)
            parent_name = getattr(parent, 'name', 'Parent Inconnu') # Bug "Parent Inconnu" sera résolu par la logique du linker
            socket_name = getattr(current_socket, 'name', 'Socket Inconnu')
            
            hop = linker.get_next_hop(current_socket)

            if not hop or hop['type'] == 'end':
                reason = hop['reason'] if hop else 'FIN DE TRACE'
                trace_table.add_row(str(step), parent_name, socket_name, f"[yellow]{reason}[/yellow]")
                break
            
            if hop['type'] == 'connection':
                next_socket = hop['next_socket']
                next_parent = linker.find_parent_for_socket(next_socket)
                cable_name = getattr(hop['via_cable'], 'name', 'N/A')
                
                # Affiche le saut complet sur une seule ligne
                trace_table.add_row(
                    str(step), parent_name, socket_name,
                    f"[green]{cable_name}[/green] -> [cyan]{getattr(next_parent, 'name', 'N/A')}[/cyan] | [bold]{getattr(next_socket, 'name', 'N/A')}[/bold]"
                )
                current_socket = next_socket

            elif hop['type'] == 'traversal':
                # AFFICHE LA TRAVERSÉE SUR UNE SEULE LIGNE COMPACTE
                device_name = getattr(hop['via_device'], 'name', 'N/A')
                trace_table.add_row(
                    str(step), parent_name,
                    f"{hop['from_socket'].name} -> {hop['to_socket'].name}",
                    f"([italic blue]Interne à {device_name}[/italic blue])"
                )
                current_socket = hop['to_socket']
            
            step += 1

        self.console.print(trace_table)
