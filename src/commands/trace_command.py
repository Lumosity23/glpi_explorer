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
        start_item = linker.find_item(self.TYPE_ALIASES.get(user_type_alias.lower()), item_name)
        if not start_item:
            self.console.print(Panel(f"Objet '{item_name}' non trouvé dans le cache.", title="[red]Erreur[/red]"))
            return

        start_sockets = linker.find_sockets_for_item(start_item)
        if not start_sockets:
            self.console.print(Panel(f"Aucun socket physique trouvé pour {start_item.name}.", border_style="yellow"))
            return

        # Pour l'instant, on prend le premier socket. Le choix interactif est pour plus tard.
        current_socket = start_sockets[0]
        
        trace_table = Table(title=f"Trace depuis {start_item.name}", expand=True)
        trace_table.add_column("Étape", justify="right")
        trace_table.add_column("Équipement")
        trace_table.add_column("Port / Traversée")
        trace_table.add_column("Via (Câble)")
        
        visited_sockets = set()
        step = 1

        while current_socket and current_socket.id not in visited_sockets:
            visited_sockets.add(current_socket.id)
            
            parent = linker.find_parent_for_socket(current_socket)
            
            # --- Traitement du hop actuel ---
            connection = linker.find_connection_for_socket(current_socket)
            if not connection:
                trace_table.add_row(str(step), getattr(parent, 'name', 'N/A'), current_socket.name, "[yellow]FIN DE LIGNE[/yellow]")
                break
            
            cable = connection['via_cable']
            next_socket = connection['other_socket']
            
            # --- Logique de traversée / concentration ---
            next_parent = linker.find_parent_for_socket(next_socket)
            
            # Cas A: Équipement passif
            if next_parent and getattr(next_parent, 'itemtype', None) == 'PassiveDCEquipment' and " IN" in next_socket.name.upper():
                out_socket = linker._get_passive_out_socket(next_parent, next_socket)
                if out_socket:
                    trace_table.add_row(
                        str(step), getattr(parent, 'name', 'N/A'), current_socket.name,
                        f"[green]{getattr(cable, 'name', 'N/A')}[/green] -> [cyan]{getattr(next_parent, 'name', 'N/A')}[/cyan] | [bold]{next_socket.name} -> {out_socket.name}[/bold]"
                    )
                    current_socket = out_socket
                    step += 1
                    continue
            
            # Cas B: Hub
            if next_parent and getattr(next_parent, 'itemtype', None) == 'NetworkEquipment' and getattr(next_parent, 'name', '').upper().startswith('HB'):
                out_socket = linker._get_hub_out_socket(next_parent)
                # Si on arrive sur un port IN, on saute au OUT
                if out_socket and next_socket != out_socket:
                    trace_table.add_row(
                        str(step), getattr(parent, 'name', 'N/A'), current_socket.name,
                        f"[green]{getattr(cable, 'name', 'N/A')}[/green] -> [cyan]{getattr(next_parent, 'name', 'N/A')}[/cyan] | [bold]{next_socket.name} -> {out_socket.name}[/bold]"
                    )
                    current_socket = out_socket
                    step += 1
                    continue

            # Cas C: Connexion normale
            trace_table.add_row(
                str(step), getattr(parent, 'name', 'N/A'), current_socket.name,
                f"[green]{getattr(cable, 'name', 'N/A')}[/green] -> [cyan]{getattr(next_parent, 'name', 'N/A')}[/cyan] | [bold]{next_socket.name}[/bold]"
            )
            current_socket = next_socket
            step += 1
        
        self.console.print(trace_table)