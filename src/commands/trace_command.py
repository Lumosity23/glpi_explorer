from .base_command import BaseCommand
from rich.panel import Panel
from rich.table import Table

class TraceCommand(BaseCommand):
    def get_help_message(self):
        return {
            "description": "Suit le chemin réseau d'un équipement de port en port.",
            "usage": "trace <type> <nom_objet>"
        }

    def execute(self, args):
        self.console.print(Panel("[yellow]La commande 'trace' est en cours de refactoring majeur et est temporairement désactivée.[/yellow]", title="[bold]Information[/bold]"))
