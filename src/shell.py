import threading
import time
import requests
from packaging.version import parse as parse_version
from rich.console import Console, Group
from rich.panel import Panel
from src.api_client import ApiClient
from src.config_manager import ConfigManager
from src.topology_cache import TopologyCache
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.formatted_text import FormattedText
import importlib
import os
from pathlib import Path
from rich.text import Text
from rich.align import Align
from rich.live import Live

class GLPIExplorerShell:
    def __init__(self):
        self.console = Console()
        self.api_client = None
        self.cache = None
        self.history = InMemoryHistory()
        self.prompt_session = PromptSession(history=self.history)
        self.commands = {}
        self.aliases = {}
        self.changelog_lock = threading.Lock()
        self.shared_state = {'shell': self, 'change_count': 0, 'changelog_lock': self.changelog_lock}
        self.is_running = False

    def _get_logo_text(self):
        logo = """ 
       ██████╗ ██╗     ██████╗ ██╗      ███████╗██╗  ██╗   
      ██╔════╝ ██║     ██╔══██╗██║      ██╔════╝╚██╗██╔╝   
    ██║  ███╗██║     ██████╔╝██║█████╗█████╗   ╚███╔╝    
    ██║   ██║██║     ██╔═══╝ ██║╚════╝██╔══╝   ██╔██╗    
        ╚██████╔╝███████╗██║     ██║      ███████╗██╔╝ ██╗██╗
         ╚═════╝ ╚══════╝╚═╝     ╚═╝      ╚══════╝╚═╝  ╚═╝╚═╝      
        """
        return Text(logo, justify="center", style="bold blue")

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

                    instance = command_class(self.api_client, self.console, self.cache, self.shared_state, self.cache.linker)
                    self.commands[command_name] = instance
                    if hasattr(instance, 'aliases') and instance.aliases:
                        for alias in instance.aliases:
                            self.aliases[alias] = command_name
                except Exception as e:
                    self.console.print(Panel(f"Avertissement: Impossible de charger la commande depuis {filename}. Erreur: {e}", title="[yellow]Chargement Commande[/yellow]"))

        try:
            from src.commands.help_command import HelpCommand
            help_instance = HelpCommand(self.api_client, self.console, self.cache, self.shared_state, self.commands, self.cache.linker)
            self.commands['help'] = help_instance
            if hasattr(help_instance, 'aliases'):
                for alias in help_instance.aliases:
                    self.aliases[alias] = 'help'
        except Exception as e:
            self.console.print(Panel(f"Avertissement: Impossible de charger la commande 'help'. Erreur: {e}", title="[yellow]Chargement Commande[/yellow]"))

    def _is_config_valid(self, config):
        if not isinstance(config, dict):
            return False
        required_keys = ["url", "app_token", "user_token"]
        return all(key in config and config[key] for key in required_keys)

    def _check_for_updates(self):
        """Vérifie s'il existe une nouvelle version sur GitHub."""
        CURRENT_VERSION = "0.1.0"
        REPO_URL = "https://api.github.com/repos/Timo-AI/GLPI-Explorer/releases/latest"
        
        try:
            response = requests.get(REPO_URL, timeout=2)
            response.raise_for_status()
            latest_version_str = response.json()['tag_name'].lstrip('v')
            
            if parse_version(latest_version_str) > parse_version(CURRENT_VERSION):
                update_message = (
                    f"Une nouvelle version ({latest_version_str}) est disponible!\n"
                    f"Pour mettre à jour, exécutez : [bold]pip install --upgrade git+https://github.com/Timo-AI/GLPI-Explorer.git[/bold]"
                )
                self.console.print(Panel(update_message, title="[bold yellow]Mise à jour disponible[/bold yellow]", border_style="yellow"))
        except (requests.exceptions.RequestException, KeyError):
            pass

    def perform_full_refresh(self, is_manual=False):
        if is_manual:
            logo_text = self._get_logo_text()
            status_text = Text("", justify="center")
            display_group = Group(logo_text, Align.center(status_text))
            panel = Panel(display_group, title="Bienvenue dans GLPI Explorer", subtitle="v0.1")

            with Live(panel, console=self.console, transient=True) as live:
                old_data = self.cache.get_all_data_copy()
                self.cache.load_from_api(self.console, live, panel, display_group)
                num_changes = self.cache.compare_and_log_changes(old_data)
                self.shared_state['change_count'] += num_changes
                self.cache.save_to_disk()
                
                final_message = f"[bold green]Rafraîchissement terminé. {num_changes} changement(s) détecté(s).[/bold green]"
                status_text = Text.from_markup(final_message, justify="center")
                display_group.renderables[1] = Align.center(status_text)
                live.update(panel)
        else:
            old_data = self.cache.get_all_data_copy()
            self.cache.load_from_api(self.console)
            num_changes = self.cache.compare_and_log_changes(old_data)
            if num_changes > 0:
                self.shared_state['change_count'] += num_changes
                self.cache.save_to_disk()

    def _run_background_refresh(self):
        while self.is_running:
            time.sleep(300)
            if self.is_running:
                with self.changelog_lock:
                    self.perform_full_refresh(is_manual=False)

    def run_single_command(self, command):
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

        cache_path = Path.home() / ".cache" / "glpi-explorer" / "topology.pkl"
        self.cache = TopologyCache.load_from_disk(cache_path, self.api_client, self.console)

        if not self.cache:
            self.console.print(Panel("[yellow]Cache non trouvé. Lancement du chargement initial...[/yellow]", title="[yellow]Avertissement[/yellow]"))
            self.cache = TopologyCache(self.api_client, cache_path)
            self.cache.load_from_api(self.console)
            self.cache.save_to_disk()
            self.console.print(Panel("[green]Chargement initial terminé.[/green]", title="[green]Succès[/green]"))

        self._load_commands()

        parts = command.split(maxsplit=1)
        command_name = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        resolved_command_name = self.aliases.get(command_name, command_name)

        self.shared_state['interactive'] = False
        if resolved_command_name in self.commands:
            self.commands[resolved_command_name].execute(args)
        else:
            self.console.print(Panel(f"[bold red]Commande inconnue:[/bold red] '{command_name}'.", title="[red]Erreur[/red]"))

        if self.api_client:
            self.api_client.close_session()

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

        cache_path = Path.home() / ".cache" / "glpi-explorer" / "topology.pkl"

        logo_text = self._get_logo_text()
        status_text = Text("", justify="center")
        display_group = Group(logo_text, Align.center(status_text))
        panel = Panel(display_group, title="Bienvenue dans GLPI Explorer", subtitle="v0.1")

        with Live(panel, console=self.console, transient=True) as live:
            status_text = Text.from_markup("[cyan]Vérification du cache local...[/cyan]", justify="center")
            display_group.renderables[1] = Align.center(status_text)
            live.update(panel)
            self.cache = TopologyCache.load_from_disk(cache_path, self.api_client, self.console)

            if self.cache:
                status_text = Text.from_markup("[green]Cache local chargé avec succès.[/green]", justify="center")
                display_group.renderables[1] = Align.center(status_text)
                live.update(panel)
                self.cache.api_client = self.api_client
                self.cache.console = self.console
            else:
                status_text = Text.from_markup("[yellow]Cache non trouvé. Lancement du chargement initial...[/yellow]", justify="center")
                display_group.renderables[1] = Align.center(status_text)
                live.update(panel)
                
                self.cache = TopologyCache(self.api_client, cache_path)
                self.cache.load_from_api(self.console, live, panel, display_group)
                self.cache.save_to_disk()

                status_text = Text.from_markup("[green]Chargement initial terminé.[/green]", justify="center")
                display_group.renderables[1] = Align.center(status_text)
                live.update(panel)

        self.console.print(panel)
        self._check_for_updates()
        self._load_commands()

        self.console.print("[dim]Lancement du service de rafraîchissement en arrière-plan...[/dim]")
        self.is_running = True
        refresh_thread = threading.Thread(target=self._run_background_refresh, daemon=True)
        refresh_thread.start()

        while True:
            try:
                change_count = self.shared_state.get('change_count', 0)
                prompt_parts = [('bold cyan', '(glpi-explorer)')]
                if change_count > 0:
                    prompt_parts.append(('', '|'))
                    prompt_parts.append(('bold yellow', f'Δ{change_count}'))
                prompt_parts.append(('', '> '))
                
                prompt_message = FormattedText(prompt_parts)
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
        
        self.is_running = False
        self.console.print("[dim]Arrêt du service de rafraîchissement... Au revoir ![/dim]")

if __name__ == "__main__":
    shell = GLPIExplorerShell()
    shell.run()
