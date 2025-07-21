from src.commands.base_command import BaseCommand
from rich.table import Table
from rich.panel import Panel

class ChangesCommand(BaseCommand):
    def __init__(self, api_client, console, cache, shared_state):
        super().__init__(api_client, console, cache, shared_state)
        self.name = "changes"
        self.description = "Affiche les changements détectés lors du dernier rafraîchissement et les efface."
        self.aliases = ["c"]

    def get_help_message(self):
        return {
            "description": "Affiche les changements détectés depuis le dernier rafraîchissement.",
            "usage": "changes"
        }

    def execute(self, args):
        lock = self.shared_state.get('changelog_lock')
        if not lock:
            self.console.print("[red]Erreur critique: Verrou de changelog manquant.[/red]")
            return

        with lock:
            changelog = self.cache.changelog
            if not changelog:
                self.console.print(Panel("Aucun changement détecté depuis le dernier rafraîchissement.", title="[blue]Information[/blue]"))
                return

            table = Table(title="Changements Détectés", expand=True)
            table.add_column("Action", style="yellow")
            table.add_column("Type")
            table.add_column("ID")
            table.add_column("Nom")
            table.add_column("Date Modif. (GLPI)", style="dim")
            table.add_column("Détails de la Modification")

            for change in changelog:
                details_str = ""
                if change['action'] == 'MODIFICATION':
                    changes = change.get('changes', {})
                    changes.pop('date_mod', None)
                    details_parts = [f"{field}: [red]{values['from']}[/red] -> [green]{values['to']}[/green]" for field, values in changes.items()]
                    details_str = "\n".join(details_parts)

                table.add_row(
                    change['action'], change['type'], str(change['id']),
                    change['name'], change.get('date_mod_glpi', 'N/A'), details_str
                )
            
            self.console.print(table)
            
            self.cache.changelog.clear()
            self.shared_state['change_count'] = 0
            self.console.print(Panel("Journal des changements effacé.", title="[dim]Nettoyage[/dim]", border_style="dim"))
