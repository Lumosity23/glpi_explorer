from src.commands.base_command import BaseCommand
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

class HelpCommand(BaseCommand):
    def __init__(self, api_client, console, cache, commands_map):
        super().__init__(api_client, console, cache)
        self.commands_map = commands_map

    def execute(self, args):
        # Table for main commands
        commands_table = Table(title="Commandes Disponibles", show_header=True, header_style="bold magenta")
        commands_table.add_column("Commande")
        commands_table.add_column("Description")
        commands_table.add_column("Usage")

        # Define aliases and their base commands
        aliases = {
            "ls": "list",
            "q": "exit",
            "cp": "compare"
        }

        # Populate commands table: list all commands that are not aliases themselves
        for cmd_name, cmd_instance in self.commands_map.items():
            # Only list actual commands, not aliases. Commands that are also base commands for aliases should be listed here.
            if cmd_name not in aliases.keys(): 
                try:
                    help_message = cmd_instance.get_help_message()
                    commands_table.add_row(cmd_name, help_message["description"], help_message["usage"])
                except Exception as e:
                    self.console.print(f"[bold red]Erreur lors de la récupération de l'aide pour {cmd_name}: {e}[/bold red]")
                    commands_table.add_row(cmd_name, "N/A", "N/A")

        # Table for aliases
        aliases_table = Table(title="Alias de Commandes", show_header=True, header_style="bold yellow")
        aliases_table.add_column("Alias")
        aliases_table.add_column("Description")
        aliases_table.add_column("Usage")

        # Populate aliases table
        for alias_name, base_command_name in aliases.items():
            # Get the help message of the base command to reference its usage
            base_command_instance = self.commands_map.get(base_command_name)
            if base_command_instance:
                try:
                    base_help_message = base_command_instance.get_help_message()
                    description = f"Alias pour la commande '{base_command_name}'"
                    # Replace the base command name with the alias name in the usage string
                    usage = base_help_message["usage"].replace(base_command_name, alias_name)
                    aliases_table.add_row(alias_name, description, usage)
                except Exception as e:
                    self.console.print(f"[bold red]Erreur lors de la récupération de l'aide pour l'alias {alias_name} (base: {base_command_name}): {e}[/bold red]")
                    aliases_table.add_row(alias_name, "N/A", "N/A")
            else:
                aliases_table.add_row(alias_name, f"Alias pour la commande '{base_command_name}' (commande de base non trouvée)", "N/A")

        # Print both tables within panels
        self.console.print(Panel(commands_table, title="[bold blue]Aide GLPI Explorer[/bold blue]"))
        self.console.print(Panel(aliases_table, title="[bold yellow]Alias[/bold yellow]"))

    def get_help_message(self):
        return {
            "description": "Affiche ce message d'aide.",
            "usage": "help"
        }
