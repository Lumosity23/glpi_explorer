from src.commands.base_command import BaseCommand
from rich.table import Table
from rich.panel import Panel
from rich.console import Group
from rich.text import Text
from rich import box

class CompareCommand(BaseCommand):
    def get_help_message(self):
        return {
            "description": "Compare et affiche les détails de deux objets GLPI l'un au-dessus de l'autre.",
            "usage": "compare <type1> <nom1> with <type2> <nom2>"
        }

    def execute(self, args):
        if " with " not in args:
            self.console.print(Panel("[bold red]Erreur:[/bold red] Syntaxe incorrecte. Utilisez 'with' pour séparer les deux objets à comparer.\nUsage: compare <type1> <nom1> with <type2> <nom2>", title="[red]Utilisation[/red]"))
            return

        parts = args.split(" with ", 1)
        item1_str = parts[0].strip()
        item2_str = parts[1].strip()

        item1_details = self._get_item_details_from_string(item1_str)
        item2_details = self._get_item_details_from_string(item2_str)

        if item1_details is None or item2_details is None:
            self.console.print(Panel("[bold red]Erreur:[/bold red] Impossible de récupérer les détails pour un ou plusieurs objets. Vérifiez les noms et les types.", title="[red]Comparaison Impossible[/red]"))
            return

        # Create a single table for comparison
        compare_table = Table(box=box.ROUNDED, show_header=False, show_edge=False, expand=True)
        compare_table.add_column("Details")

        # Render item 1 details
        display_object_1 = self._render_item_details_to_display_object(item1_details["details"], item1_details["glpi_itemtype"])
        compare_table.add_row(Panel(display_object_1, title=f"[bold blue]{item1_details["canonical_item_name"]}[/bold blue]", box=box.MINIMAL))

        # Add a section separator
        compare_table.add_section()

        # Render item 2 details
        display_object_2 = self._render_item_details_to_display_object(item2_details["details"], item2_details["glpi_itemtype"])
        compare_table.add_row(Panel(display_object_2, box=box.MINIMAL))

        self.console.print(Panel(compare_table, title="[bold cyan]Comparaison d'Équipements GLPI[/bold cyan]"))

    def _get_item_details_from_string(self, item_string):
        try:
            user_type_alias, item_name = item_string.split(maxsplit=1)
        except ValueError:
            self.console.print(Panel(f"[bold red]Erreur:[/bold red] Syntaxe incorrecte pour l'objet '{item_string}'. Attendu: <type> <nom_objet>", title="[red]Utilisation[/red]"))
            return None

        glpi_itemtype = self.TYPE_ALIASES.get(user_type_alias.lower())
        
        if not glpi_itemtype:
            self.console.print(Panel(f"[bold red]Erreur:[/bold red] Le type '{user_type_alias}' est inconnu.", title="[red]Type Inconnu[/red]"))
            return None
        
        with self.console.status(f"Récupération de la liste des '{glpi_itemtype}'..."):
            all_items = self.api_client.list_items(glpi_itemtype, item_range="0-9999")

        if not all_items:
            self.console.print(Panel(f"Aucun objet de type '{user_type_alias}' trouvé dans GLPI.", title="[blue]Information[/blue]", border_style="blue"))
            return None

        found_item = None
        for item in all_items:
            if item.get("name", "").lower() == item_name.lower():
                found_item = item
                break
        
        if found_item is None:
            self.console.print(Panel(f"Erreur: Aucun objet de type '{user_type_alias}' nommé '{item_name}' trouvé.", title="[red]Non trouvé[/red]"))
            return None

        item_id = found_item.get("id")
        canonical_item_name = found_item.get("name", item_name)

        with self.console.status(f"Récupération des détails de {canonical_item_name}..."):
            details = self.api_client.get_item_details(glpi_itemtype, item_id)
        
        if details:
            return {
                "details": details,
                "glpi_itemtype": glpi_itemtype,
                "canonical_item_name": canonical_item_name
            }
        else:
            self.console.print(Panel(f"[bold red]Erreur:[/bold red] Impossible de récupérer les détails pour '{canonical_item_name}'.", title="[red]Erreur[/red]"))
            return None
