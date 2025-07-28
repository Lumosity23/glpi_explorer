from src.commands.base_command import BaseCommand
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

class MapCommand(BaseCommand):
    def __init__(self, api_client, console, cache, shared_state=None, linker=None):
        super().__init__(api_client, console, cache, shared_state)
        self.linker = linker
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
        
        sockets = getattr(item, 'sockets', [])
        if not sockets:
            self.console.print(Panel("[bold yellow]Aucun socket trouvé pour cet équipement.[/bold yellow]", title="[yellow]Information[/yellow]"))
            return
            
        table = Table(title="Sockets Disponibles", show_header=True, header_style="bold magenta")
        table.add_column("Num", style="cyan", justify="right")
        table.add_column("Nom", style="white")
        table.add_column("Statut", style="yellow")
        table.add_column("Connecté à", style="blue")
        
        for i, socket in enumerate(sockets):
            status = "Libre"
            connected_to = "N/A"

            if getattr(socket, 'connection', None):
                status = "Connecté"
                conn_socket = socket.connection.get('to_socket')
                if conn_socket and getattr(conn_socket, 'parent', None):
                    connected_to = f"{conn_socket.parent.name} (Socket {getattr(conn_socket, 'name', conn_socket.id)})"
            
            table.add_row(
                str(i + 1),
                getattr(socket, 'name', str(getattr(socket, 'id', 'N/A'))),
                status,
                connected_to
            )
        
        self.console.print(table)

    def _interactive_map_session(self, current_item):
        while True:
            # Traverse automatiquement les équipements passifs
            while getattr(current_item, 'itemtype', None) == 'PassiveDCEquipment':
                sockets = getattr(current_item, 'sockets', [])
                out_socket = next(
                    (s for s in sockets if " OUT" in getattr(s, 'name', '').upper() and self.linker.find_connection_for_socket(s)),
                    None
                )
                if not out_socket:
                    self.console.print(Panel(f"[yellow]Aucun port OUT connecté trouvé sur {current_item.name}.[/yellow]", title="[yellow]Fin de Ligne[/yellow]"))
                    return
                in_socket = self._get_passive_in_socket(current_item, out_socket)
                if not in_socket:
                    self.console.print(Panel(f"[yellow]Impossible de trouver le port IN correspondant à {out_socket.name} sur {current_item.name}.[/yellow]", title="[yellow]Fin de Ligne[/yellow]"))
                    return
                connection = self.linker.find_connection_for_socket(in_socket)
                if not connection:
                    self.console.print(Panel(f"[yellow]Le port IN {in_socket.name} n'est pas connecté.[/yellow]", title="[yellow]Fin de Ligne[/yellow]"))
                    return
                next_socket = connection['other_socket']
                parent = self.linker.find_parent_for_socket(next_socket)
                if not parent or parent == current_item:
                    self.console.print(Panel("Arrêt : Parent du socket introuvable ou boucle détectée. La trace s'est perdue.", title="[red]Erreur de Topologie[/red]"))
                    return
                # Affiche la notification unique, maintenant correcte
                next_device_name = getattr(parent, 'name', '???')
                self.console.print(
                    Panel(
                        f"[cyan]Traverse automatiquement :[/cyan] [bold]{current_item.name}[/bold] via [bold]{out_socket.name}/IN[/bold] → [green]{next_device_name}[/green]",
                        title="[cyan]Passif traversé[/cyan]"
                    )
                )
                current_item = parent

            # Ici, current_item est actif : on affiche et on demande à l'utilisateur
            self._display_map(current_item)
            sockets = getattr(current_item, 'sockets', [])
            choice = Prompt.ask(
                "[bold green]Choisissez un numéro de socket pour explorer (ou 'q' pour quitter, 'b' pour revenir à l'équipement précédent)[/bold green]",
                choices=[str(i+1) for i in range(len(sockets))] + ['q', 'b']
            )

            if choice.lower() == 'q':
                self.console.print(Panel("[bold yellow]Fin de l'exploration.[/bold yellow]", title="[yellow]Session Terminée[/yellow]"))
                break
            elif choice.lower() == 'b':
                self.console.print(Panel("[bold yellow]Fonctionnalité 'retour' non implémentée pour l'instant.[/bold yellow]", title="[yellow]Information[/yellow]"))
                continue
            else:
                try:
                    idx = int(choice) - 1
                    selected_socket = sockets[idx]
                    connection = self.linker.find_connection_for_socket(selected_socket)
                    if not connection:
                        self.console.print(Panel("[yellow]Ce socket n'est pas connecté.[/yellow]"))
                        continue
                    next_socket = connection['other_socket']
                    parent = self.linker.find_parent_for_socket(next_socket)
                    if not parent:
                        self.console.print(Panel("Arrêt : Parent du socket introuvable. La trace s'est perdue.", title="[red]Erreur de Topologie[/red]"))
                        return
                    current_item = parent
                except (ValueError, IndexError):
                    self.console.print(Panel("[bold red]Erreur:[/bold red] Choix invalide. Veuillez entrer un numéro valide, 'q' ou 'b'.", title="[red]Erreur[/red]"))

    def _get_passive_in_socket(self, passive_equip, out_socket):
        # Cherche le port IN correspondant à un port OUT
        if " OUT" not in out_socket.name.upper():
            return None
        in_name = out_socket.name.upper().replace(" OUT", " IN")
        sockets_on_passive = getattr(passive_equip, 'sockets', [])
        return next((s for s in sockets_on_passive if s.name.upper() == in_name), None)

