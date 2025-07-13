from src.commands.base_command import BaseCommand
from rich.panel import Panel
from src.api_client import ApiClient

class DebugCommand(BaseCommand):
    def get_help_message(self):
        return {
            "description": "Active le mode débogage pour une commande spécifique (non implémenté).",
            "usage": "debug <commande> [args]"
        }

    def execute(self, args):
        self.console.print(Panel(f"[bold yellow]Mode Débogage:[/bold yellow] Commande reçue: [cyan]debug {args}[/cyan]", title="[yellow]DEBUG[/yellow]"))
        # La commande debug devra elle-même instancier et appeler la commande appropriée (ex: GetCommand) en lui passant un flag de débogage.
        # Pour l'instant, nous allons juste afficher le message de débogage.
        # TODO: Implémenter l'appel aux autres commandes avec un flag de débogage.



