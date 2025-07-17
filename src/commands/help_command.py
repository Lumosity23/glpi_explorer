from src.commands.base_command import BaseCommand
from rich.table import Table
from rich.panel import Panel

class HelpCommand(BaseCommand):
    def __init__(self, api_client, console, cache, commands_map):
        super().__init__(api_client, console, cache)
        self.commands_map = commands_map
        self.aliases = ["h"]

    def execute(self, args):
        # Table for main commands
        commands_table = Table(title="Commandes Disponibles", show_header=True, header_style="bold magenta")
        commands_table.add_column("Commande")
        commands_table.add_column("Description")
        commands_table.add_column("Usage")

        # Table for aliases
        aliases_table = Table(title="Alias de Commandes", show_header=True, header_style="bold yellow")
        aliases_table.add_column("Alias")
        aliases_table.add_column("Commande de Base")
        aliases_table.add_column("Description")

        # Add exit/quit command info
        commands_table.add_row("exit", "Quitte l'application.", "exit, quit, q")

        # Populate commands and aliases tables
        for cmd_name, cmd_instance in sorted(self.commands_map.items()):
            try:
                help_message = cmd_instance.get_help_message()
                commands_table.add_row(cmd_name, help_message["description"], help_message["usage"])
                
                # Check for aliases and add them to the aliases table
                if hasattr(cmd_instance, 'aliases') and cmd_instance.aliases:
                    for alias in cmd_instance.aliases:
                        aliases_table.add_row(alias, cmd_name, help_message["description"])

            except Exception as e:
                self.console.print(f"[bold red]Erreur lors de la récupération de l'aide pour {cmd_name}: {e}[/bold red]")
                commands_table.add_row(cmd_name, "N/A", "N/A")

        # Print both tables within panels
        self.console.print(Panel(commands_table, title="[bold blue]Aide GLPI Explorer[/bold blue]"))
        if aliases_table.row_count > 0:
            self.console.print(Panel(aliases_table, title="[bold yellow]Alias[/bold yellow]"))

    def get_help_message(self):
        return {
            "description": "Affiche ce message d'aide.",
            "usage": "help"
        }
