from rich.console import Console
from rich.panel import Panel
from src.api_client import ApiClient
from src.config_manager import ConfigManager
from src.topology_cache import TopologyCache
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.formatted_text import FormattedText
import importlib
import os

class GLPIExplorerShell:
    def __init__(self):
        self.console = Console()
        self.api_client = None
        self.cache = None
        self.history = InMemoryHistory()
        self.prompt_session = PromptSession(history=self.history)
        self.commands = {}
        self.aliases = {}

    def _load_commands(self):
        self.commands = {}
        self.aliases = {}
        commands_dir = os.path.join(os.path.dirname(__file__), 'commands')

        for filename in os.listdir(commands_dir):
            if filename.endswith('_command.py') and not filename.startswith('base'):
                module_name = filename[:-3]
                command_name = module_name.replace('_command', '')
                try:
                    module = importlib.import_module(f'src.commands.{module_name}')
                    class_name = ''.join(word.capitalize() for word in command_name.replace('_', ' ').split()) + 'Command'
                    command_class = getattr(module, class_name)

                    if command_name == 'help':
                        continue

                    instance = command_class(self.api_client, self.console, self.cache)
                    self.commands[command_name] = instance
                    if hasattr(instance, 'aliases') and instance.aliases:
                        for alias in instance.aliases:
                            self.aliases[alias] = command_name
                except Exception as e:
                    self.console.print(Panel(f"Avertissement: Impossible de charger la commande depuis {filename}. Erreur: {e}", title="[yellow]Chargement Commande[/yellow]"))

        try:
            from src.commands.help_command import HelpCommand
            self.commands['help'] = HelpCommand(self.api_client, self.console, self.cache, self.commands)
        except Exception as e:
            self.console.print(Panel(f"Avertissement: Impossible de charger la commande 'help'. Erreur: {e}", title="[yellow]Chargement Commande[/yellow]"))

    def _is_config_valid(self, config):
        if not isinstance(config, dict):
            return False
        required_keys = ["url", "app_token", "user_token"]
        return all(key in config and config[key] for key in required_keys)

    def run(self):
        config_manager = ConfigManager()
        config = config_manager.load_config()

        if not self._is_config_valid(config):
            self.console.print(Panel("[bold blue]Configuration requise.[/bold blue]", expand=False))
            config = config_manager.run_setup_interactive()
            config_manager.save_config(config)

        self.api_client = ApiClient(config)
        if not self.api_client.connect():
            self.console.print(Panel("[bold red]Échec de la connexion.[/bold red]", title="[red]Erreur[/red]"))
            return

        self.cache = TopologyCache(self.api_client)
        self.cache.load_from_api(self.console)
        self._load_commands()

        while True:
            try:
                prompt_message = FormattedText([('bold cyan', '(glpi-explorer)> ')])
                full_command = self.prompt_session.prompt(prompt_message).strip()

                if not full_command:
                    continue
                
                parts = full_command.split(maxsplit=1)
                command_name = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""

                if command_name in ('exit', 'quit', 'q'):
                    if self.api_client:
                        self.api_client.close_session()
                    break

                resolved_command_name = self.aliases.get(command_name, command_name)

                if resolved_command_name in self.commands:
                    self.commands[resolved_command_name].execute(args)
                else:
                    supported_cmds = ", ".join(sorted(list(self.commands.keys()) + list(self.aliases.keys())))
                    self.console.print(Panel(f"[bold red]Commande inconnue:[/bold red] '{command_name}'.", title="[red]Erreur[/red]"))

            except EOFError:
                if self.api_client:
                    self.api_client.close_session()
                break

if __name__ == "__main__":
    shell = GLPIExplorerShell()
    shell.run()