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
            status = "[red]Libre[/red]"
            connected_to = "N/A"

            # On utilise le linker pour trouver la connexion
            connection = self.linker.find_connection_for_socket(socket)
            if connection:
                status = "[green]Connecté[/green]"
                other_socket = connection['other_socket']
                other_parent = self.linker.find_parent_for_socket(other_socket)
                if other_parent:
                    connected_to = f"{other_parent.name} (Socket {other_socket.name})"
                else:
                    connected_to = f"Socket {other_socket.name} (Parent Inconnu)"

            table.add_row(
                str(i + 1),
                getattr(socket, 'name', str(getattr(socket, 'id', 'N/A'))),
                status,
                connected_to
            )
        
        self.console.print(table)

    def _interactive_map_session(self, start_item):
        # --- NOUVEAU : Initialisation de l'historique ---
        navigation_history = [start_item] # Pile pour le 'back'
        path_taken = [] # Liste pour le récapitulatif final

        current_item = start_item
        while True:
            self._display_map(current_item)

            # --- NOUVEAU : Logique de fin de trace ---
            if getattr(current_item, 'itemtype', None) == 'Computer':
                self.console.print(Panel("[bold green]Destination terminale atteinte.[/bold green]\nOptions: 'b' pour revenir, 'q' pour quitter et voir le récapitulatif.", title="[green]Fin de Trace[/green]"))
                choices = ['b', 'q']
            else:
                sockets = getattr(current_item, 'sockets', [])
                choices = [str(i+1) for i in range(len(sockets))] + ['b', 'q']

            choice = Prompt.ask("Votre choix", choices=choices, show_choices=False)

            if choice.lower() == 'q':
                self.console.print(Panel("Fin de l'exploration.", title="Session Terminée"))
                # --- NOUVEAU : Afficher le récapitulatif ---
                self._display_path_summary(path_taken)
                break
            
            elif choice.lower() == 'b':
                # --- NOUVEAU : Gérer le retour ---
                if len(navigation_history) > 1:
                    navigation_history.pop() # Enlever l'actuel
                    current_item = navigation_history[-1] # Revenir au précédent
                    if path_taken:
                        path_taken.pop() # Enlever le dernier saut du récap
                else:
                    self.console.print("[yellow]Vous êtes déjà au point de départ.[/yellow]")
                continue

            else:
                try:
                    idx = int(choice) - 1
                    sockets = getattr(current_item, 'sockets', [])
                    selected_socket = sockets[idx]
                    
                    # --- DÉBUT DE LA NOUVELLE LOGIQUE DE "SOUS-TRACE" ---
                    
                    # On stocke le point de départ de ce saut
                    path_step = {'from_device': current_item, 'from_socket': selected_socket}
                    
                    current_hop_socket = selected_socket
                    traversed_passives = [] # Pour stocker les passifs traversés

                    # Boucle de traversée
                    while True:
                        connection = self.linker.find_connection_for_socket(current_hop_socket)
                        if not connection:
                            self.console.print(Panel(f"[yellow]Le port {current_hop_socket.name} n'est pas connecté. Fin du saut.[/yellow]"))
                            current_item = getattr(current_hop_socket, 'parent', current_item)
                            break 

                        next_socket = connection['other_socket']
                        next_parent = self.linker.find_parent_for_socket(next_socket)

                        if not next_parent:
                            self.console.print(Panel("Arrêt : Parent du socket introuvable. La trace s'est perdue.", title="[red]Erreur de Topologie[/red]"))
                            return
                        
                        if getattr(next_parent, 'itemtype', None) != 'PassiveDCEquipment':
                            # On est arrivé sur un équipement actif ou un terminal, on s'arrête
                            current_item = next_parent
                            path_step['to_device'] = current_item
                            path_step['to_socket'] = next_socket
                            break 
                        
                        # C'est un passif, on le traverse
                        traversed_passives.append(f"{next_parent.name} (Socket {next_socket.name})")
                        exit_socket = self.linker.get_next_hop_for_map(next_socket).get('to_socket')
                        
                        if not exit_socket:
                            self.console.print(Panel(f"Arrêt : impossible de trouver le port de sortie sur {next_parent.name}", title="[red]Erreur[/red]"))
                            current_item = next_parent
                            break
                        
                        current_hop_socket = exit_socket
                    
                    # Afficher les notifications de traversée
                    if traversed_passives:
                        path_str = " -> ".join(traversed_passives)
                        self.console.print(Panel(f"Bypass automatique via : {path_str}", title="[dim]Traversée[/dim]"))
                    
                    # Mettre à jour l'historique pour le récapitulatif
                    path_taken.append(path_step)
                    navigation_history.append(current_item)
                    # --- FIN DE LA NOUVELLE LOGIQUE ---

                except (ValueError, IndexError):
                    self.console.print(Panel("[bold red]Erreur:[/bold red] Choix invalide.", title="[red]Erreur[/red]"))

    def _display_path_summary(self, path):
        if not path:
            return
        
        summary_table = Table(title="Récapitulatif de votre Exploration")
        summary_table.add_column("Étape", style="cyan")
        summary_table.add_column("Équipement de Départ", style="green")
        summary_table.add_column("Port de Sortie", style="yellow")
        summary_table.add_column("Équipement d'Arrivée", style="green")
        summary_table.add_column("Port d'Entrée", style="yellow")
        
        for i, step in enumerate(path):
            summary_table.add_row(
                str(i + 1),
                f"{step['from_device'].name} ({step['from_device'].itemtype})",
                step['from_socket'].name,
                f"{step['to_device'].name} ({step['to_device'].itemtype})",
                step['to_socket'].name
            )
        
        self.console.print(summary_table)

    def _get_passive_in_socket(self, passive_equip, out_socket):
        # Cherche le port IN correspondant à un port OUT
        if " OUT" not in out_socket.name.upper():
            return None
        in_name = out_socket.name.upper().replace(" OUT", " IN")
        sockets_on_passive = getattr(passive_equip, 'sockets', [])
        return next((s for s in sockets_on_passive if s.name.upper() == in_name), None)

