# src/commands/testlink_command.py
from .base_command import BaseCommand
from ..topology_linker import TopologyLinker # Notez l'import relatif
from rich.panel import Panel

class TestlinkCommand(BaseCommand):
    def __init__(self, api_client, console, cache):
        super().__init__(api_client, console, cache)
        self.name = "testlink"
        self.description = "Teste un lien de topologie à partir d'un ID de socket."
        self.aliases = ["tl"]

    def get_help_message(self):
        return {
            "description": self.description,
            "usage": "testlink <socket_id>"
        }

    def execute(self, args):
        try:
            socket_id = int(args)
        except (ValueError, TypeError):
            self.console.print(Panel("Usage: testlink <socket_id_numerique>", title="[red]Erreur[/red]"))
            return

        # Créer une instance du linker avec le cache
        linker = TopologyLinker(self.cache)

        # Étape 1: Trouver le socket de départ
        start_socket = linker.find_socket_by_id(socket_id)
        if not start_socket:
            self.console.print(Panel(f"Socket ID {socket_id} non trouvé dans le cache.", title="[red]Erreur[/red]"))
            return
        
        self.console.print(f"Socket de départ trouvé: [cyan]{start_socket.name}[/cyan]")

        # Étape 2: Trouver la connexion
        connection = linker.find_connection_for_socket(start_socket)

        if not connection:
            self.console.print(Panel(f"Aucune connexion trouvée pour le socket {start_socket.name}", title="[yellow]Fin de Ligne[/yellow]"))
            return

        cable = connection['via_cable']
        other_socket = connection['other_socket']

        self.console.print(f"  -> Connecté via le câble: [magenta]{cable.name}[/magenta]")
        self.console.print(f"  -> À l'autre socket: [cyan]{other_socket.name}[/cyan]")
