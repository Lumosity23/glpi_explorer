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

        start_ports = getattr(start_item, 'ports', [])
        if not start_ports:
            self.console.print(Panel(f"Aucun port trouvé pour {start_item.name} dans le cache.", border_style="yellow"))
            return

        # Pour cette mission, on part du premier port
        current_port = start_ports[0]
        
        trace_table = Table(title=f"Trace depuis {start_item.name}", expand=True)
        trace_table.add_column("Étape")
        trace_table.add_column("Équipement")
        trace_table.add_column("Port")
        trace_table.add_column("Câble")
        trace_table.add_column("Équipement Suivant")
        trace_table.add_column("Port Suivant")

        step = 1
        visited_ports = set()
        
        while current_port and current_port.id not in visited_ports:
            visited_ports.add(current_port.id)
            
            parent = getattr(current_port, 'parent', None)
            socket = getattr(current_port, 'socket', None)
            connection = getattr(socket, 'connection', None) if socket else None
            
            parent_name = getattr(parent, 'name', 'N/A')
            port_name = getattr(current_port, 'name', 'N/A')
            
            if connection:
                cable = connection['via_cable']
                next_socket = connection['to_socket']
                next_port = getattr(next_socket, 'port', None)
                next_parent = getattr(next_port, 'parent', None) if next_port else getattr(next_socket, 'parent', None)

                trace_table.add_row(
                    str(step), parent_name, port_name,
                    getattr(cable, 'name', 'N/A'),
                    getattr(next_parent, 'name', 'N/A'),
                    getattr(next_port, 'name', 'N/A')
                )
                current_port = next_port # On passe au port logique suivant
            else:
                trace_table.add_row(str(step), parent_name, port_name, "[yellow]FIN DE LIGNE[/yellow]", "", "")
                current_port = None # Arrêt de la boucle
            
            step += 1
            
        self.console.print(trace_table)
