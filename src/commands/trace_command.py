from .base_command import BaseCommand
from rich.panel import Panel
from rich.table import Table

class TraceCommand(BaseCommand):
    def get_help_message(self):
        return {
            "description": "Suit le chemin réseau d'un équipement de port en port.",
            "usage": "trace <type> <nom_objet>"
        }

    def execute(self, args):
        # --- ÉTAPE 1: Analyse des arguments et recherche de l'objet de départ ---
        try:
            user_type_alias, item_name = args.split(maxsplit=1)
        except ValueError:
            self.console.print(Panel("Usage: trace <type> <nom_objet>", title="[red]Erreur[/red]"))
            return
        
        glpi_itemtype = self.TYPE_ALIASES.get(user_type_alias.lower())
        if not glpi_itemtype:
            self.console.print(Panel(f"Type inconnu : '{user_type_alias}'", title="[red]Erreur[/red]"))
            return

        # Recherche directe et explicite dans le bon dictionnaire du cache
        target_dict = None
        if glpi_itemtype == 'Computer': target_dict = self.cache.computers
        elif glpi_itemtype == 'NetworkEquipment': target_dict = self.cache.network_equipments
        elif glpi_itemtype == 'PassiveDCEquipment': target_dict = self.cache.passive_devices
        
        start_item = None
        if target_dict:
            for item in target_dict.values():
                if getattr(item, 'name', '').lower() == item_name.lower():
                    start_item = item
                    break
        
        if not start_item:
            self.console.print(Panel(f"Objet '{item_name}' non trouvé dans le cache.", title="[red]Erreur[/red]"))
            return

        # --- ÉTAPE 2: Initialisation de la trace ---
        trace_table = Table(title=f"Trace depuis {start_item.name}", expand=True)
        trace_table.add_column("Étape")
        trace_table.add_column("Équipement")
        trace_table.add_column("Socket/Port")
        trace_table.add_column("Via Câble")
        trace_table.add_column("Vers Équipement")
        trace_table.add_column("Vers Socket/Port")

        # La clé est d'utiliser getattr pour accéder à l'attribut que le cache est censé avoir ajouté
        start_ports = getattr(start_item, 'networkports', [])
        
        if not start_ports:
            self.console.print(Panel(f"Aucun port réseau trouvé pour {start_item.name}. Fin de la trace.", border_style="yellow"))
            return

        # Pour l'instant, on prend le premier port logique trouvé
        current_port = start_ports[0]
        current_socket = getattr(current_port, 'socket', None)
        
        if not current_socket:
            self.console.print(Panel(f"Le port {current_port.name} n'a pas de socket physique associé. Fin de la trace.", border_style="yellow"))
            return
        
        # --- ÉTAPE 3: Boucle de traçage ---
        visited_sockets = set()
        step = 1
        while current_socket and current_socket.id not in visited_sockets:
            visited_sockets.add(current_socket.id)
            
            parent_equip = getattr(current_socket, 'parent_item', None)
            parent_name = getattr(parent_equip, 'name', 'N/A')
            
            cable = getattr(current_socket, 'via_cable', None)
            cable_name = getattr(cable, 'name', 'N/A')
            
            next_socket = getattr(current_socket, 'connected_to', None)
            
            if next_socket:
                next_parent = getattr(next_socket, 'parent_item', None)
                next_parent_name = getattr(next_parent, 'name', 'N/A')
                
                trace_table.add_row(
                    str(step), parent_name, current_socket.name,
                    f"[green]{cable_name}[/green]",
                    next_parent_name, next_socket.name
                )
                current_socket = next_socket # Passe au socket suivant
            else:
                trace_table.add_row(
                    str(step), parent_name, current_socket.name,
                    f"[yellow]FIN DE LIGNE[/yellow]", "", ""
                )
                current_socket = None # Arrête la boucle
            
            step += 1

        self.console.print(trace_table)
