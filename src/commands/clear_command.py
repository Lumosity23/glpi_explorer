import os
from src.commands.base_command import BaseCommand

class ClearCommand(BaseCommand):
    def __init__(self, api_client, console, cache):
        super().__init__(api_client, console, cache)
        self.aliases = ["cls"]
        
    def get_help_message(self):
        return {
            "description": "Nettoie l'écran du terminal.",
            "usage": "clear"
        }

    def execute(self, args):
        """Clears the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')