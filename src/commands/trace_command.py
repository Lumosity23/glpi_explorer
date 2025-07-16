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

        trace_table = Table(title=f"Trace depuis {start_item.name}", expand=True)
        trace_table.add_column("Étape")
        trace_table.add_column("Équipement Début")
        trace_table.add_column("Port Début")
        trace_table.add_column("Câble")
        trace_table.add_column("Équipement Fin")
        trace_table.add_column("Port Fin")
        
        # Utiliser le linker pour construire le chemin
        path = linker.build_path_from_item(start_item)

        if not path:
            self.console.print(Panel(f"Impossible de démarrer une trace depuis {start_item.name}. Vérifiez ses connexions.", border_style="yellow"))
            return

        # Afficher le chemin
        for step, hop in enumerate(path, 1):
            trace_table.add_row(
                str(step),
                hop.get('start_equip_name', 'N/A'),
                hop.get('start_port_name', 'N/A'),
                hop.get('cable_name', 'N/A'),
                hop.get('end_equip_name', 'N/A'),
                hop.get('end_port_name', 'N/A'),
            )
        
        self.console.print(trace_table)
