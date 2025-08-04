# src/commands/trace_command.py
from .base_command import BaseCommand
from ..topology_linker import TopologyLinker
from rich.panel import Panel
from rich.table import Table

class TraceCommand(BaseCommand):
    def __init__(self, api_client, console, cache, shared_state, linker=None):
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
        device_type_colors = {}
        colors = ["cyan", "magenta", "yellow", "green", "blue", "red"]
        device_colors = ["white", "bright_red", "bright_green", "bright_blue", "bright_magenta", "bright_yellow"]
        color_index = 0
        device_color_index = 0

        while current_socket and current_socket.id not in visited_sockets:
            visited_sockets.add(current_socket.id)
            parent = linker.find_parent_for_socket(current_socket)

            # --- Localisation color ---
            location_name = "N/A"
            if parent:
                location_id = getattr(parent, 'locations_id', None)
                if location_id and location_id in self.cache.locations:
                    # On récupère le nom complet de la localisation
                    location_obj = self.cache.locations[location_id]
                    location_name = getattr(location_obj, 'name', str(location_id))
                elif location_id:
                    location_name = str(location_id)

            if location_name not in location_colors:
                location_colors[location_name] = colors[color_index % len(colors)]
                color_index += 1
            loc_color = location_colors[location_name]

            # --- Device type color ---
            device_type = getattr(parent, 'type', 'default')
            if device_type not in device_type_colors:
                device_type_colors[device_type] = device_colors[device_color_index % len(device_colors)]
                device_color_index += 1
            dev_color = device_type_colors[device_type]

            hop = linker.get_next_hop(current_socket)

            if not hop or hop['type'] == 'end':
                trace_table.add_row(
                    str(step),
                    f"[{loc_color}]{location_name}[/{loc_color}]",
                    f"[{dev_color}]{getattr(parent, 'name', 'N/A')}[/{dev_color}]",
                    current_socket.name,
                    f"[yellow]{hop.get('reason', 'FIN') if hop else 'FIN'}[/yellow]"
                )
                break

            if hop['type'] == 'connection':
                next_socket = hop['next_socket']
                next_parent = linker.find_parent_for_socket(next_socket)
                trace_table.add_row(
                    str(step),
                    f"[{loc_color}]{location_name}[/{loc_color}]",
                    f"[{dev_color}]{getattr(parent, 'name', 'N/A')}[/{dev_color}]",
                    current_socket.name,
                    f"[green]{getattr(hop['via_cable'], 'name', 'N/A')}[/green] -> [cyan]{getattr(next_parent, 'name', 'N/A')}[/cyan]"
                )
                current_socket = next_socket

            elif hop['type'] == 'traversal':
                trace_table.add_row(
                    str(step),
                    f"[{loc_color}]{location_name}[/{loc_color}]",
                    f"[{dev_color}]{getattr(parent, 'name', 'N/A')}[/{dev_color}]",
                    f"{current_socket.name} -> {hop['to'].name}",
                    f"([italic blue]Interne[/italic blue])"
                )
                current_socket = hop['to']

            step += 1
            
        self.console.print(trace_table)