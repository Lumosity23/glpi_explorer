
import os
import json
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

class ConfigManager:
    def __init__(self):
        self.config_path = Path.home() / ".config" / "glpi-explorer" / "config.json"

    def load_config(self):
        if self.config_path.exists():
            with open(self.config_path, "r") as f:
                return json.load(f)
        return None

    def save_config(self, config_data):
        os.makedirs(self.config_path.parent, exist_ok=True)
        with open(self.config_path, "w") as f:
            json.dump(config_data, f, indent=4)

    def run_setup_interactive(self):
        console = Console()
        console.print(Panel("[bold blue]Configuration de l'API GLPI[/bold blue]", expand=False))
        glpi_url = Prompt.ask("Veuillez entrer l'URL de l'API GLPI")
        app_token = Prompt.ask("Veuillez entrer l'App-Token")
        user_token = Prompt.ask("Veuillez entrer le User-Token")
        return {"url": glpi_url, "app_token": app_token, "user_token": user_token}


