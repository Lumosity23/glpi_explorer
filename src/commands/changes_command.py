from src.commands.base_command import BaseCommand
from rich.table import Table
from rich.panel import Panel

class ChangesCommand(BaseCommand):
    def __init__(self, api_client, console, cache, shared_state):
        super().__init__(api_client, console, cache, shared_state)
        self.name = "changes"
        self.description = "Affiche les changements détectés lors du dernier rafraîchissement et les efface."
        self.aliases = ["c"]

    def execute(self, args=None):
        if not self.cache.changelog:
            self.console.print(Panel("[bold yellow]Aucun changement détecté depuis le dernier rafraîchissement.[/bold yellow]", title="[yellow]Changements[/yellow]"))
            return

        table = Table(title="[bold blue]Changements Détectés[/bold blue]", show_header=True, header_style="bold magenta")
        table.add_column("Action", style="cyan", justify="left")
        table.add_column("Type", style="green", justify="left")
        table.add_column("ID", style="yellow", justify="right")
        table.add_column("Nom", style="white", justify="left")

        for change in self.cache.changelog:
            action_style = "bold green" if change['action'] == 'AJOUT' else "bold red"
            table.add_row(
                f"[{action_style}]{change['action']}[/{action_style}]",
                change['type'],
                str(change['id']),
                change['name']
            )
        
        self.console.print(table)
        
        # Clear the changelog and reset the change count
        self.cache.changelog.clear()
        self.shared_state['change_count'] = 0
        self.console.print(Panel("[dim]Journal des changements effacé.[/dim]", title="[dim]Nettoyage[/dim]"))
