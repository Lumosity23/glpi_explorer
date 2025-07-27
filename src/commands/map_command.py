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
            self._display_map(current_item)

            sockets = getattr(current_item, 'sockets', [])
            choice = Prompt.ask("[bold green]Choisissez un numéro de socket pour explorer (ou 'q' pour quitter, 'b' pour revenir à l'équipement précédent)[/bold green]", choices=[str(i+1) for i in range(len(sockets))] + ['q', 'b'])

            if choice.lower() == 'q':
                self.console.print(Panel("[bold yellow]Fin de l'exploration.[/bold yellow]", title="[yellow]Session Terminée[/yellow]"))
                break
            elif choice.lower() == 'b':
                self.console.print(Panel("[bold yellow]Fonctionnalité 'retour' non implémentée pour l'instant.[/bold yellow]", title="[yellow]Information[/yellow]"))
                continue # Rester sur le même équipement pour l'instant
            else:
                try:
                    idx = int(choice) - 1
                    selected_socket = sockets[idx]
                    
                    connection = self.linker.find_connection_for_socket(selected_socket)
                    if not connection:
                        self.console.print(Panel("[yellow]Ce socket n'est pas connecté.[/yellow]"))
                        continue

                    next_socket = connection['other_socket']
                    
                    # --- DÉBUT DE LA NOUVELLE LOGIQUE DE TRAVERSÉE ---
                    
                    current_hop_socket = next_socket
                    
                    # On boucle TANT QUE l'équipement suivant est un passif
                    while True:
                        parent = self.linker.find_parent_for_socket(current_hop_socket)
                        if not parent or getattr(parent, 'itemtype', None) != 'PassiveDCEquipment':
                            # On est arrivé sur un équipement actif ou une fin de ligne, on arrête la traversée
                            current_item = parent
                            break

                        self.console.print(Panel(f"Arrivée sur [cyan]{parent.name}[/cyan] | Port [cyan]{current_hop_socket.name}[/cyan]... Traversée automatique.", title="[dim]Navigation[/dim]"))

                        # On trouve le port de sortie
                        exit_socket = self.linker._get_passive_traversal_socket(parent, current_hop_socket)
                        if not exit_socket:
                            self.console.print(Panel(f"Arrêt : impossible de trouver le port de sortie sur {parent.name}", title="[red]Erreur de Topologie[/red]"))
                            current_item = None
                            break

                        # On trouve la connexion du port de sortie
                        next_connection = self.linker.find_connection_for_socket(exit_socket)
                        if not next_connection:
                            self.console.print(Panel(f"Arrêt : le port de sortie {exit_socket.name} n'est pas connecté.", title="[yellow]Fin de Ligne[/yellow]"))
                            current_item = exit_socket.parent
                            break
                            
                        current_hop_socket = next_connection['other_socket']

                    if not current_item:
                        self.console.print(Panel("La trace s'est perdue. Retour à l'équipement précédent.", title="[red]Erreur[/red]"))
                        # Ne pas changer 'current_item' pour rester au même endroit
                    
                except (ValueError, IndexError):
                    self.console.print(Panel("[bold red]Erreur:[/bold red] Choix invalide. Veuillez entrer un numéro valide, 'q' ou 'b'.", title="[red]Erreur[/red]"))

