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
            shell.perform_full_refresh(is_manual_refresh=True)
        else:
            self.console.print("[red]Erreur: Impossible d'accéder au shell pour le rafraîchissement.[/red]")