from src.commands.base_command import BaseCommand
from rich.table import Table
from rich.panel import Panel
from rich.console import Group
from rich.text import Text
from rich import box
from src.api_client import ApiClient

class GetCommand(BaseCommand):
    def __init__(self, api_client, console, cache):
        super().__init__(api_client, console, cache)

    def get_help_message(self):
        return {
            "description": "Récupère et affiche les détails d'un objet GLPI spécifique ou d'un port.",
            "usage": "get <type> <nom_objet> | get port <nom_port> on <nom_equipement>"
        }

    def execute(self, args):
        if not args:
            self.console.print(Panel("[bold red]Erreur:[/bold red] La commande 'get' nécessite des arguments.\nUsage: get <type> <nom_objet> | get port <nom_port> on <nom_equipement>", title="[red]Utilisation[/red]"))
            return

        parts = args.split(maxsplit=1)
        command_type = parts[0].lower()

        if command_type == "port":
            self._get_port_details(parts[1] if len(parts) > 1 else "")
        else:
            self._get_item_details(args)

    def _get_item_details(self, args):
        try:
            user_type_alias, item_name = args.split(maxsplit=1)
        except ValueError:
            self.console.print(Panel("[bold red]Erreur:[/bold red] Syntaxe incorrecte. Il manque soit le type, soit le nom de l'objet.\nUsage: get <type> <nom_objet>", title="[red]Utilisation[/red]"))
            return

        glpi_itemtype = self.TYPE_ALIASES.get(user_type_alias.lower())
        if not glpi_itemtype:
            self.console.print(Panel(f"Erreur: Type d'objet inconnu '{user_type_alias}'.", title="Erreur de commande", style="bold red"))
            return

        target_dict = self.get_target_dict(glpi_itemtype)
        
        details = None
        if target_dict:
            for item in target_dict.values():
                if getattr(item, 'name', '').lower() == item_name.lower():
                    details = item
                    break
        
        if details:
            self._display_item_details(details, glpi_itemtype)
        else:
            self.console.print(Panel(f"Erreur: Aucun objet de type '{glpi_itemtype}' nommé '{item_name}' trouvé dans le cache.", title="Erreur", style="bold red"))

    def _get_port_details(self, args):
        self.console.print(Panel("[yellow]La commande 'get port' est en cours de refactoring majeur et est temporairement désactivée.[/yellow]", title="[bold]Information[/bold]"))