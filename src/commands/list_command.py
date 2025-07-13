from src.commands.base_command import BaseCommand
from rich.table import Table
from rich.panel import Panel
from rich import box
from src.api_client import ApiClient

class ListCommand(BaseCommand):
    def get_help_message(self):
        return {
            "description": "Liste les objets GLPI d'un type donné.",
            "usage": "list <type>"
        }

    def execute(self, args):
        if not args:
            help_table = Table(title="[bold blue]Types disponibles pour la commande `list`[/bold blue]")
            help_table.add_column("Type disponible", style="cyan")
            help_table.add_column("Alias", style="magenta")

            seen_aliases = set()
            for alias, item_type in self.TYPE_ALIASES.items():
                if item_type not in seen_aliases:
                    aliases_for_type = [a for a, t in self.TYPE_ALIASES.items() if t == item_type]
                    help_table.add_row(item_type, ", ".join(aliases_for_type))
                    seen_aliases.add(item_type)
            
            self.console.print(Panel(help_table, expand=False))
            return
        
        user_type_alias = args.lower()
        glpi_itemtype = self.TYPE_ALIASES.get(user_type_alias)
        if not glpi_itemtype:
            self.console.print(Panel(f"[bold red]Erreur:[/bold red] Type inconnu: \'{user_type_alias}\'", title="[red]Erreur[/red]"))
            return
            
        with self.console.status(f"Liste des objets de type {glpi_itemtype}..."):
            items = self.api_client.list_items(glpi_itemtype)
        
        if not items:
            self.console.print(Panel(f"Aucun objet de type \'{user_type_alias}\' n\'a été trouvé dans GLPI.", title="[blue]Information[/blue]", border_style="blue"))
            return
        
        table = Table(
            title=f"Liste des {glpi_itemtype}",
            box=box.ROUNDED,
            header_style="bold magenta",
            show_edge=False,
            title_style="bold blue"
        )
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Nom", style="magenta")
        table.add_column("Statut", style="green") # Always add Statut
        
        if glpi_itemtype == "Cable":
            table.add_column("Type Câble", style="yellow")

        for item in items:
            row_data = [
                str(item.get("id", "N/A")),
                item.get("name", "N/A"),
                str(item.get("states_id", "N/A")) # Always include Statut
            ]
            if glpi_itemtype == "Cable":
                row_data.append(item.get("cabletypes_id", "N/A"))
            table.add_row(*row_data)
        self.console.print(Panel(table, expand=False))




