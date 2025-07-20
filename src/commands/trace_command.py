# src/commands/trace_command.py
from .base_command import BaseCommand
from ..topology_linker import TopologyLinker
from rich.panel import Panel
from rich.table import Table

class TraceCommand(BaseCommand):
    def __init__(self, api_client, console, cache, shared_state):
        super().__init__(api_client, console, cache, shared_state)
        self.aliases = ["tr"]
        self.last_trace_result = []

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
        
        trace_table = Table(title=f"Trace depuis {start_item.name}", expand=True, show_lines=True)
        trace_table.add_column("Étape", justify="right")
        trace_table.add_column("Localisation")
        trace_table.add_column("Équipement")
        trace_table.add_column("Port")
        trace_table.add_column("Via")

        visited_sockets = set()
        step = 1
        
        # --- NOUVELLE LOGIQUE DE COULEURS ---
        location_colors = {}
        colors = ["cyan", "magenta", "yellow", "green", "blue", "red"]
        color_index = 0

        while current_socket and current_socket.id not in visited_sockets:
            visited_sockets.add(current_socket.id)
            parent = linker.find_parent_for_socket(current_socket)
            
            # --- Attribution des couleurs ---
            location_name = getattr(parent, 'locations_id', 'N/A')
            if location_name not in location_colors:
                location_colors[location_name] = colors[color_index % len(colors)]
                color_index += 1
            loc_style = location_colors[location_name]
            
            # --- Logique d'affichage ---
            hop = linker.get_next_hop(current_socket)
            
            via_info = ""
            next_socket_for_loop_check = None

            if hop and hop['type'] == 'connection':
                next_socket = hop['next_socket']
                next_parent = linker.find_parent_for_socket(next_socket)
                cable_name = getattr(hop['via_cable'], 'name', 'N/A')
                via_info = f"[green]{cable_name}[/green] -> [{loc_style}]{getattr(next_parent, 'name', 'N/A')}[/{loc_style}]"
                next_socket_for_loop_check = next_socket
            elif hop and hop['type'] == 'traversal':
                via_info = f"([italic {loc_style}]Traversée de {getattr(hop['via_device'], 'name', 'N/A')}[/italic {loc_style}])"
                next_socket_for_loop_check = hop['to_socket']
            else:
                via_info = f"[bold yellow]{hop.get('reason', 'FIN DE TRACE') if hop else 'FIN DE TRACE'}[/bold yellow]"

            trace_table.add_row(
                str(step),
                f"[{loc_style}]{location_name}[/{loc_style}]",
                f"[{loc_style}]{getattr(parent, 'name', 'N/A')}[/{loc_style}]",
                current_socket.name,
                via_info
            )

            # --- GESTION DE LA FIN DE TRACE ---
            if not hop or hop['type'] == 'end':
                break # On s'arrête proprement
            
            if next_socket_for_loop_check and next_socket_for_loop_check.id in visited_sockets:
                trace_table.add_row("", "", "", "", "[bold red]BOUCLE DÉTECTÉE -> FIN[/bold red]")
                break

            if hop['type'] == 'connection':
                current_socket = hop['next_socket']
            elif hop['type'] == 'traversal':
                current_socket = hop['to_socket']
            
            step += 1
                
        self.console.print(trace_table)