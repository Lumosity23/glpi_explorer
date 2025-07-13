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
    def __init__(self, console=None):
        self.console = console if console else Console()
        self.api_client = None
        self.cache = None
        self.history = InMemoryHistory()
        self.prompt_session = PromptSession(history=self.history)
        self.commands = {}
        # Command loading is now deferred to the run method

    def _load_commands(self):
        self.commands = {}
        commands_dir = os.path.join(os.path.dirname(__file__), 'commands')

        # Dynamically load all command classes from the 'commands' directory
        for filename in os.listdir(commands_dir):
            if filename.endswith('_command.py') and not filename.startswith('base_'):
                module_name = f"src.commands.{filename[:-3]}"
                class_name_snake = filename.replace('.py', '')
                class_name_camel = "".join(word.capitalize() for word in class_name_snake.split('_'))

                try:
                    module = importlib.import_module(module_name)
                    command_class = getattr(module, class_name_camel)
                    
                    command_name = class_name_snake.replace('_command', '')

                    # Special constructor for commands needing the cache
                    if command_name in ('trace', 'debug'):
                        instance = command_class(self.api_client, self.console, self.cache)
                    # Special constructor for help command
                    elif command_name == 'help':
                        instance = command_class(self.api_client, self.console, self.commands)
                    else:
                        instance = command_class(self.api_client, self.console)

                    self.commands[command_name] = instance
                    
                    # Add aliases if they exist
                    if hasattr(instance, 'aliases'):
                        for alias in instance.aliases:
                            self.commands[alias] = instance

                except (ImportError, AttributeError) as e:
                    self.console.print(f"[bold red]WARNING: Could not load command from {filename}: {e}[/bold red]")

        # Post-load processing for commands that need the full command map (like 'help')
        if 'help' in self.commands:
            help_instance = self.commands['help']
            if hasattr(help_instance, 'set_commands'):
                help_instance.set_commands(self.commands)

    def _is_config_valid(self, config):
        if not isinstance(config, dict):
            return False
        required_keys = ["url", "app_token", "user_token"]
        for key in required_keys:
            if key not in config or not config[key]:
                return False
        return True

    def run(self):
        config_manager = ConfigManager()
        config = config_manager.load_config()

        if not self._is_config_valid(config):
            self.console.print(Panel("[bold blue]Bienvenue... ou la configuration est invalide.[/bold blue]\n[yellow]Il semble que ce soit votre première utilisation ou que la configuration précédente soit manquante ou corrompue.\nNous allons vous guider à travers le processus de configuration.[/yellow]", expand=False))
            while True:
                config = config_manager.run_setup_interactive()
                api_client_test = ApiClient(config)
                with self.console.status("[bold green]Test de la connexion API...[/bold green]"):
                    is_connected = api_client_test.connect()

                if not is_connected:
                    self.console.print(Panel(f"[bold red]Échec de la connexion :[/bold red] Veuillez réessayer avec des informations valides.", title="[red]Erreur de Connexion[/red]"))
                else:
                    api_client_test.close_session()
                    config_manager.save_config(config)
                    self.console.print(Panel("[bold green]Configuration sauvegardée avec succès ![/bold green]", title="[green]Succès[/green]"))
                    break

        self.api_client = ApiClient(config)
        with self.console.status("[bold green]Connexion à l'API GLPI...[/bold green]"):
            is_connected = self.api_client.connect()

        if not is_connected:
            self.console.print(Panel(f"[bold red]Échec de la connexion principale :[/bold red] Veuillez vérifier votre configuration ou relancer l'application pour reconfigurer.", title="[red]Erreur[/red]"))
            return

        # Initialize and load cache
        self.cache = TopologyCache(self.api_client)
        self.cache.load_from_api(self.console)

        # Load commands now that api_client is initialized
        self._load_commands()

        self.console.print(Panel("Bienvenue dans GLPI Explorer", title="[bold cyan]GLPI Explorer[/]", subtitle="[green]v0.1[/]"))

        while True:
            try:
                prompt_message = FormattedText([
                    ('bold cyan', '(glpi-explorer)> ')
                ])
                
                full_command = self.prompt_session.prompt(prompt_message).strip()

                if not full_command:
                    continue
                parts = full_command.split(maxsplit=1)
                command_name = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""

                # Handle aliases
                if command_name == "ls":
                    command_name = "list"
                elif command_name == "q":
                    command_name = "exit"

                if command_name in self.commands:
                    command_instance = self.commands[command_name]
                    command_instance.execute(args)
                elif command_name in ("exit", "quit"):
                    if self.api_client:
                        self.api_client.close_session()
                    break
                else:
                    self.console.print(Panel(f"[bold red]Commande inconnue:[/bold red] '{command_name}'. Commandes supportées: {', '.join(self.commands.keys())}, exit, quit, ls, q", title="[red]Erreur[/red]"))

            except EOFError:
                if self.api_client:
                    self.api_client.close_session()
                break