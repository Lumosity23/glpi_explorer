from src.commands.base_command import BaseCommand
from rich.table import Table
from rich.panel import Panel
from rich.console import Group
from rich.text import Text
from rich import box
from src.api_client import ApiClient

class GetCommand(BaseCommand):
    def __init__(self, api_client, console, cache, shared_state, linker=None):
        super().__init__(api_client, console, cache, shared_state)
        self.aliases = ["show"]

    def get_help_message(self):
        return {
            "description": "Récupère les détails d'un objet, d'un port, ou d'une étape de trace.",
            "usage": "get <type> <nom> | get port <nom> on <equip> | get step <num>"
        }

    def execute(self, args):
        if not args:
            self.console.print(Panel("[bold red]Erreur:[/bold red] La commande 'get' nécessite des arguments.", title="[red]Utilisation[/red]"))
            return

        parts = args.split(maxsplit=1)
        command_type = parts[0].lower()

        if command_type == "port":
            self._get_port_details(parts[1] if len(parts) > 1 else "")
        elif command_type == "step":
            self._get_step_details(parts[1] if len(parts) > 1 else "")
        else:
            self._get_item_details(args)

    def _get_step_details(self, args):
        try:
            step_number = int(args)
            last_trace = self.shared_state.get('last_trace', [])
            if 1 <= step_number <= len(last_trace):
                step_data = last_trace[step_number - 1]
                
                parent_panel = Panel(self._render_item_details_to_display_object(step_data['parent'], step_data['parent'].itemtype), title="Équipement")
                
                socket_table = Table(title="Port / Socket", box=box.MINIMAL)
                socket_table.add_column("Attribut")
                socket_table.add_column("Valeur")
                socket_table.add_row("Nom", step_data['socket'].name)
                socket_table.add_row("ID", str(step_data['socket'].id))
                socket_panel = Panel(socket_table)

                cable = step_data.get('hop', {}).get('via_cable')
                cable_panel = Panel("N/A")
                if cable:
                    cable_panel = Panel(self._render_item_details_to_display_object(cable, 'Cable'), title="Câble")

                self.console.print(parent_panel, socket_panel, cable_panel)

            else:
                self.console.print(f"[red]Numéro d'étape invalide. La dernière trace avait {len(last_trace)} étapes.[/red]")
        except (ValueError, IndexError):
            self.console.print("[red]Usage: get step <numero>[/red]")

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
            display_object = self._render_item_details_to_display_object(details, glpi_itemtype)
            self.console.print(display_object)
        else:
            self.console.print(Panel(f"Erreur: Aucun objet de type '{glpi_itemtype}' nommé '{item_name}' trouvé dans le cache.", title="Erreur", style="bold red"))

    def _get_port_details(self, args):
        self.console.print(Panel("[yellow]La commande 'get port' est en cours de refactoring majeur et est temporairement désactivée.[/yellow]", title="[bold]Information[/bold]"))