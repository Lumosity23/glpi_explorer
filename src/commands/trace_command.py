from .base_command import BaseCommand
from rich.panel import Panel
from rich.table import Table
from ..topology_linker import TopologyLinker

class TraceCommand(BaseCommand):
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

        start_ports = linker.find_ports_for_item(start_item)
        if not start_ports:
            self.console.print(Panel(f"Aucun port réseau trouvé pour {start_item.name}. Fin de la trace.", border_style="yellow"))
            return

        start_socket = linker.find_socket_for_port(start_ports[0])
        if not start_socket:
            self.console.print(Panel(f"Le port {start_ports[0].name} n'a pas de socket physique associé. Fin de la trace.", border_style="yellow"))
            return

        trace_table = Table(title=f"Trace depuis {start_item.name}", expand=True)
        trace_table.add_column("Étape")
        trace_table.add_column("Équipement")
        trace_table.add_column("Socket/Port")
        trace_table.add_column("Via Câble")
        trace_table.add_column("Vers Équipement")
        trace_table.add_column("Vers Socket/Port")

        current_hop_socket = start_socket
        step = 1
        visited_sockets = set()

        while current_hop_socket and current_hop_socket.id not in visited_sockets:
            visited_sockets.add(current_hop_socket.id)
            parent = linker._find_parent_of_socket(current_hop_socket)
            parent_name = getattr(parent, 'name', 'N/A')

            connection = linker.find_connection_for_socket(current_hop_socket)
            if connection:
                cable_name = getattr(connection['via_cable'], 'name', 'N/A')
                next_socket = connection['other_socket']
                next_parent = linker._find_parent_of_socket(next_socket)
                next_parent_name = getattr(next_parent, 'name', 'N/A')
                next_socket_name = getattr(next_socket, 'name', 'N/A')

                trace_table.add_row(
                    str(step),
                    parent_name,
                    current_hop_socket.name,
                    f"[green]{cable_name}[/green]",
                    next_parent_name,
                    next_socket_name
                )
                current_hop_socket = linker.get_next_hop(current_hop_socket)
            else:
                trace_table.add_row(
                    str(step), parent_name, current_hop_socket.name,
                    f"[yellow]FIN DE LIGNE[/yellow]", "", ""
                )
                current_hop_socket = None
            
            step += 1

        self.console.print(trace_table)
