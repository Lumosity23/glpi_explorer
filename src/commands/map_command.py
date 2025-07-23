from src.commands.base_command import BaseCommand
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

class MapCommand(BaseCommand):
    def __init__(self, api_client, console, cache, shared_state=None):
        super().__init__(api_client, console, cache, shared_state)
        self.name = "map"
        self.description = "Explore la topologie réseau à partir d'un équipement."
        self.aliases = ["m"]

    def get_help_message(self):
        return {
            "description": "Explore la topologie réseau à partir d'un équipement donné, en permettant de naviguer de port en port.",
            "usage": "map <type_equipement> <nom_equipement>"
        }

    def execute(self, args):
        if not args:
            self.console.print(Panel("[bold red]Erreur:[/bold red] Veuillez spécifier le type et le nom de l'équipement de départ. Ex: map computer PC001", title="[red]Erreur[/red]"))
            return

        parts = args.split(maxsplit=1)
        if len(parts) < 2:
            self.console.print(Panel("[bold red]Erreur:[/bold red] Format incorrect. Ex: map computer PC001", title="[red]Erreur[/red]"))
            return

        item_type_str = parts[0].lower()
        item_name = parts[1]

        # Traduire l'alias en type GLPI réel
        item_type = self.get_item_type_from_alias(item_type_str)
        if not item_type:
            self.console.print(Panel(f"[bold red]Erreur:[/bold red] Type d'équipement inconnu: {item_type_str}", title="[red]Erreur[/red]"))
            return

        # Rechercher l'équipement de départ dans le cache
        start_item = None
        if item_type == 'Computer':
            for item in self.cache.computers.values():
                if getattr(item, 'name', '').lower() == item_name.lower():
                    start_item = item
                    break
        elif item_type == 'NetworkEquipment':
            for item in self.cache.network_equipments.values():
                if getattr(item, 'name', '').lower() == item_name.lower():
                    start_item = item
                    break
        elif item_type == 'PassiveDCEquipment':
            for item in self.cache.passive_devices.values():
                if getattr(item, 'name', '').lower() == item_name.lower():
                    start_item = item
                    break
        
        if not start_item:
            self.console.print(Panel(f"[bold red]Erreur:[/bold red] Équipement '{item_name}' de type '{item_type_str}' non trouvé dans le cache.", title="[red]Erreur[/red]"))
            return

        self.console.print(Panel(f"[bold green]Démarrage de l'exploration de la topologie à partir de:[/bold green] {start_item.name} ({start_item.itemtype})", title="[green]Exploration Topologique[/green]"))
        if self.shared_state.get('interactive', True):
            self._interactive_map_session(start_item)
        else:
            self._display_map(start_item)

    def _display_map(self, item):
        self.console.print(Panel(f"[bold blue]Équipement Actuel:[/bold blue] {item.name} ({item.itemtype})", title="[blue]Navigation[/blue]"))
        
        ports = getattr(item, 'ports', [])
        sockets = getattr(item, 'sockets', [])

        if not ports and not sockets:
            self.console.print(Panel("[bold yellow]Aucun port ou socket trouvé pour cet équipement.[/bold yellow]", title="[yellow]Information[/yellow]"))
            return

        table = Table(title="Ports et Sockets Disponibles", show_header=True, header_style="bold magenta")
        table.add_column("Num", style="cyan", justify="right")
        table.add_column("Type", style="green")
        table.add_column("Nom", style="white")
        table.add_column("Statut", style="yellow")
        table.add_column("Connecté à", style="blue")

        display_items = []
        for p in ports:
            display_items.append({'type': 'Port', 'obj': p})
        for s in sockets:
            display_items.append({'type': 'Socket', 'obj': s})
        
        for i, item_info in enumerate(display_items):
            item_type = item_info['type']
            item_obj = item_info['obj']
            
            status = "Libre"
            connected_to = "N/A"

            if item_type == 'Port':
                if getattr(item_obj, 'socket', None):
                    socket = item_obj.socket
                    if getattr(socket, 'connection', None):
                        status = "Connecté"
                        conn_socket = socket.connection.get('to_socket')
                        if conn_socket and getattr(conn_socket, 'parent', None):
                            connected_to = f"{conn_socket.parent.name} (Port/Socket {getattr(conn_socket, 'name', conn_socket.id)})"
            elif item_type == 'Socket':
                if getattr(item_obj, 'connection', None):
                    status = "Connecté"
                    conn_socket = item_obj.connection.get('to_socket')
                    if conn_socket and getattr(conn_socket, 'parent', None):
                        connected_to = f"{conn_socket.parent.name} (Port/Socket {getattr(conn_socket, 'name', conn_socket.id)})"
            
            table.add_row(
                str(i + 1),
                item_type,
                getattr(item_obj, 'name', str(getattr(item_obj, 'id', 'N/A'))),
                status,
                connected_to
            )
        
        self.console.print(table)

    def _interactive_map_session(self, current_item):
        while True:
            self._display_map(current_item)

            choice = Prompt.ask("[bold green]Choisissez un numéro de port/socket pour explorer (ou 'q' pour quitter, 'b' pour revenir à l'équipement précédent)[/bold green]", choices=[str(i+1) for i in range(len(getattr(current_item, 'ports', [])) + len(getattr(current_item, 'sockets', [])))] + ['q', 'b'])

            if choice.lower() == 'q':
                self.console.print(Panel("[bold yellow]Fin de l'exploration.[/bold yellow]", title="[yellow]Session Terminée[/yellow]"))
                break
            elif choice.lower() == 'b':
                self.console.print(Panel("[bold yellow]Fonctionnalité 'retour' non implémentée pour l'instant.[/bold yellow]", title="[yellow]Information[/yellow]"))
                continue # Rester sur le même équipement pour l'instant
            else:
                try:
                    idx = int(choice) - 1
                    display_items = []
                    ports = getattr(current_item, 'ports', [])
                    sockets = getattr(current_item, 'sockets', [])
                    for p in ports:
                        display_items.append({'type': 'Port', 'obj': p})
                    for s in sockets:
                        display_items.append({'type': 'Socket', 'obj': s})

                    selected_item_info = display_items[idx]
                    selected_obj = selected_item_info['obj']

                    if getattr(selected_obj, 'connection', None):
                        next_socket = selected_obj.connection.get('to_socket')
                        if next_socket and getattr(next_socket, 'parent', None):
                            current_item = next_socket.parent
                        else:
                            self.console.print(Panel("[bold red]Erreur:[/bold red] Impossible de trouver l'équipement connecté à ce port/socket.", title="[red]Erreur de Navigation[/red]"))
                    else:
                        self.console.print(Panel("[bold yellow]Ce port/socket n'est pas connecté à un autre équipement.[/bold yellow]", title="[yellow]Information[/yellow]"))

                except (ValueError, IndexError):
                    self.console.print(Panel("[bold red]Erreur:[/bold red] Choix invalide. Veuillez entrer un numéro valide, 'q' ou 'b'.", title="[red]Erreur[/red]"))

