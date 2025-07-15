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
            self.console.print(Panel(f"[bold red]Erreur:[/bold red] Le type '{user_type_alias}' est inconnu.", title="[red]Type Inconnu[/red]"))
            return
        
        with self.console.status(f"Récupération de la liste des '{glpi_itemtype}'..."):
            all_items = self.api_client.list_items(glpi_itemtype, item_range="0-9999")

        if not all_items:
            self.console.print(Panel(f"Aucun objet de type '{user_type_alias}' trouvé dans GLPI.", title="[blue]Information[/blue]", border_style="blue"))
            return

        found_item = None
        for item in all_items:
            if item.get("name", "").lower() == item_name.lower():
                found_item = item
                break
        
        if found_item is None:
            self.console.print(Panel(f"Erreur: Aucun objet de type '{user_type_alias}' nommé '{item_name}' trouvé.", title="[red]Non trouvé[/red]"))
            return

        item_id = found_item.get("id")
        canonical_item_name = found_item.get("name", item_name)

        with self.console.status(f"Récupération des détails de {canonical_item_name}..."):
            details = self.api_client.get_item_details(glpi_itemtype, item_id)
        
        if details:
            display_object = self._render_item_details_to_display_object(details, glpi_itemtype)
            self.console.print(Panel(display_object, title=f"[bold blue]Détails de {canonical_item_name}[/bold blue]"))
        else:
            self.console.print(Panel(f"[bold red]Erreur:[/bold red] Impossible de récupérer les détails pour '{canonical_item_name}'.", title="[red]Erreur[/red]"))

    def _get_port_details(self, args):
        self.console.print(Panel("[yellow]La commande 'get port' est en cours de refactoring majeur et est temporairement désactivée.[/yellow]", title="[bold]Information[/bold]"))