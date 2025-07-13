import os
from src.commands.base_command import BaseCommand

class ClearCommand(BaseCommand):
    def get_help_message(self):
        return {
            "description": "Nettoie l'écran du terminal.",
            "usage": "clear"
        }

    def execute(self, args):
        """Clears the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')