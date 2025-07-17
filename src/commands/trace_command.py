from .base_command import BaseCommand
from rich.panel import Panel
from rich.table import Table
from ..topology_linker import TopologyLinker

class TraceCommand(BaseCommand):
    def __init__(self, api_client, console, cache):
        super().__init__(api_client, console, cache)
        self.aliases = ["tr"]

    def get_help_message(self):
        return {
            "description": "Suit le chemin réseau d'un équipement de port en port.",
            "usage": "trace <type> <nom_objet>"
        }

    def execute(self, args):
        try:
            user_type_alias, item_name = args.split(maxsplit=1)
        except ValueError:
            self.console.print(Panel("Usage: trace <type> <nom_objet>", title="[red]Erreur[/red]"))
            return

        glpi_itemtype = self.TYPE_ALIASES.get(user_type_alias.lower())
        if not glpi_itemtype:
            self.console.print(Panel(f"Type inconnu : '{user_type_alias}'", title="[red]Erreur[/red]"))
            return

        linker = TopologyLinker(self.cache)
        start_item = linker.find_item(glpi_itemtype, item_name)

        if not start_item:
            self.console.print(Panel(f"Objet '{item_name}' non trouvé dans le cache.", title="[red]Erreur[/red]"))
            return

        start_item_id = getattr(start_item, 'id', None)
        if not start_item_id:
            self.console.print(Panel(f"Impossible de trouver l'ID pour {start_item.name}", title="[red]Erreur[/red]"))
            return

        # --- ÉTAPE 1: Trouver les sockets de départ CORRECTEMENT ---
        start_sockets = self.cache.get_sockets_for_item_id(start_item_id)
        if not start_sockets:
            self.console.print(Panel(f"Aucun socket physique trouvé pour {start_item.name} via l'index. Fin de la trace.", border_style="yellow"))
            return

        # Pour l'instant, on prend le premier socket. Le choix interactif sera pour une future mission.
        current_socket = start_sockets[0]
        
        # --- ÉTAPE 2: Initialisation et Boucle de traçage ---
        trace_table = Table(title=f"Trace depuis {start_item.name}", expand=True)
        trace_table.add_column("Étape")
        trace_table.add_column("Équipement")
        trace_table.add_column("Socket")
        trace_table.add_column("Câble")
        trace_table.add_column("Équipement Suivant")
        trace_table.add_column("Socket Suivant")
        
        visited_sockets = set()
        step = 1

        while current_socket and current_socket.id not in visited_sockets:
            visited_sockets.add(current_socket.id)
            
            parent = getattr(current_socket, 'parent_item', None)
            parent_name = getattr(parent, 'name', 'Parent Inconnu')
            
            connection = linker.find_connection_for_socket(current_socket) # Utiliser la méthode du cache
            
            if connection:
                cable_name = getattr(connection['via_cable'], 'name', 'N/A')
                next_socket_initial = connection['other_socket']
                next_parent = getattr(next_socket_initial, 'parent_item', None)
                next_parent_name = getattr(next_parent, 'name', 'Parent Inconnu')
                
                trace_table.add_row(
                    str(step), parent_name, current_socket.name,
                    f"[green]{cable_name}[/green]",
                    next_parent_name, next_socket_initial.name
                )

                # --- NOUVELLE LOGIQUE DE TRAVERSÉE ---
                # Est-ce qu'on a atterri sur un passif ?
                if getattr(next_parent, 'itemtype', None) == 'PassiveDCEquipment':
                    if " IN" in next_socket_initial.name.upper():
                        out_port_name = next_socket_initial.name.upper().replace(" IN", " OUT")
                        # Trouver le port OUT correspondant sur le MÊME équipement passif
                        out_socket = next((s for s in self.cache.sockets.values() if getattr(s, 'parent_item', None) == next_parent and s.name.upper() == out_port_name), None)
                        
                        if out_socket:
                            trace_table.add_row("", f"-> Traversée de {next_parent_name}", f"{next_socket_initial.name} -> {out_socket.name}", "(Interne)", "", "")
                            current_socket = out_socket # Le prochain saut partira du port OUT
                        else:
                            current_socket = None # Arrêt si pas de port OUT
                    else: # Si on arrive sur un OUT, on continue normalement
                        current_socket = next_socket_initial
                else: # Si ce n'est pas un passif, on continue normalement
                    current_socket = next_socket_initial

            else: # Fin de la ligne
                trace_table.add_row(str(step), parent_name, current_socket.name, "[yellow]FIN DE LIGNE[/yellow]", "", "")
                current_socket = None
            
            step += 1
            
        self.console.print(trace_table)
