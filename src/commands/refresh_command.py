# src/commands/refresh_command.py
from .base_command import BaseCommand
from rich.panel import Panel

class RefreshCommand(BaseCommand):
    def __init__(self, api_client, console, cache, shared_state=None):
        super().__init__(api_client, console, cache, shared_state)
        self.aliases = ["r"]

    def get_help_message(self):
        return {
            "description": "Met à jour le cache local en rechargeant toutes les données depuis l'API GLPI.",
            "usage": "refresh"
        }

    def execute(self, args):
        shell = self.shared_state.get('shell')
        if shell:
            change_count = self.cache.refresh_from_api(self.console)
            self.shared_state['change_count'] = change_count
            self.console.print(Panel(f"[bold green]Le cache a été mis à jour avec succès depuis GLPI.[/bold green]\n{change_count} changements détectés.", title="[green]Rafraîchissement Terminé[/green]"))
        else:
            self.console.print("[red]Erreur: Impossible d'accéder au shell pour le rafraîchissement.[/red]")