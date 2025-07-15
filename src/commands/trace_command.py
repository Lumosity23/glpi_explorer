from src.commands.base_command import BaseCommand
from rich.table import Table
from rich.panel import Panel
from rich.console import Console
from rich import box

class TraceCommand(BaseCommand):
    def __init__(self, api_client, console, cache):
        super().__init__(api_client, console, cache)
        self.name = "trace"
        self.description = "Trace a network path from a starting device through the topology cache."
        self.aliases = ["t"]

    def execute(self, args):
        if not args:
            self._display_error("Usage: trace <item_type> <item_name>")
            return

        parts = args.split(maxsplit=1)
        if len(parts) < 2:
            self._display_error("Usage: trace <item_type> <item_name>")
            return

        item_type_alias, item_name = parts
        item_type = self._get_item_type(item_type_alias)

        self.console.print(f"Starting trace for {item_name}")
        start_item = self._find_item_in_cache(item_type, item_name)

        if not start_item:
            self._display_error(f"Item '{item_name}' of type '{item_type}' not found in cache.")
            return

        self.console.print(f"Found start item: {start_item.name}")
        print(f"[DEBUG] ID of start_item: {id(start_item)}")
        if item_type == 'Computer':
            cached_item = self.cache.computers.get(start_item.id)
            if cached_item:
                print(f"[DEBUG] ID of cached_item (from self.cache.computers): {id(cached_item)}")
                print(f"[DEBUG] Are they the same object? {start_item is cached_item}")
                print(f"[DEBUG] networkports on cached_item: {getattr(cached_item, 'networkports', 'Attribute not found')}")
                print(f"[DEBUG] len(networkports on cached_item): {len(getattr(cached_item, 'networkports', []))}")
            else:
                print(f"[DEBUG] Cached item not found in self.cache.computers for ID {start_item.id}")
        self._perform_trace(start_item, item_type)

    def _find_item_in_cache(self, item_type, item_name):
        """Finds an item in the cache by its type and name."""
        target_cache_dict = None
        if item_type == 'Computer':
            target_cache_dict = self.cache.computers
        elif item_type == 'NetworkEquipment':
            target_cache_dict = self.cache.network_equipments
        elif item_type == 'PassiveDCEquipment':
            target_cache_dict = self.cache.passive_dc_equipments
        # Add other types as needed
        
        if target_cache_dict:
            for item in target_cache_dict.values():
                if item.name.lower() == item_name.lower():
                    return item
        return None

    def _perform_trace(self, start_item, start_itemtype):
        trace_table = Table(title=f"Trace depuis {start_item.name}", expand=True)
        # Définir les colonnes de la table
        trace_table.add_column("Étape", justify="right")
        trace_table.add_column("Équipement")
        trace_table.add_column("Socket/Port")
        trace_table.add_column("Connecté via")
        trace_table.add_column("Vers Équipement")
        trace_table.add_column("Vers Socket/Port")

        # --- ÉTAPE 1: Point de Départ ---
        # Extraire les ports de l'objet équipement du cache
        start_ports_data = start_item._networkports.get('NetworkPortEthernet', [])
        if not start_ports_data:
            self.console.print(Panel("Aucun port réseau trouvé pour cet équipement.", border_style="yellow"))
            return
        
        # Pour l'instant, on prend le premier port. Plus tard, on mettra un menu interactif.
        start_port_data = start_ports_data[0]
        current_port = self.cache.network_ports.get(start_port_data['id'])
        current_socket = getattr(current_port, 'socket', None)
        
        visited_sockets = set()
        step = 1

        # --- ÉTAPE 2: Boucle de Traçage ---
        while current_socket and current_socket.id not in visited_sockets:
            visited_sockets.add(current_socket.id)
            
            parent_equip = getattr(current_socket, 'parent_item', None)
            parent_name = getattr(parent_equip, 'name', 'Parent Inconnu')
            
            next_socket = getattr(current_socket, 'connected_to', None)
            via_cable_name = getattr(getattr(current_socket, 'via_cable', None), 'name', 'N/A')
            
            # Si le port a une destination
            if next_socket:
                next_parent_equip = getattr(next_socket, 'parent_item', None)
                next_parent_name = getattr(next_parent_equip, 'name', 'Parent Inconnu')
                
                trace_table.add_row(
                    str(step),
                    parent_name,
                    current_socket.name,
                    f"[green]{via_cable_name}[/green]",
                    next_parent_name,
                    next_socket.name
                )
                
                # --- ÉTAPE 3: Logique de Traversée ---
                # Si la destination est un équipement passif (Patch Panel, Wall Outlet)
                if getattr(next_parent_equip, 'itemtype', None) == 'PassiveDCEquipment':
                    if " IN" in next_socket.name.upper():
                        out_port_name = next_socket.name.upper().replace(" IN", " OUT")
                        # On cherche le port de sortie sur le même équipement passif
                        out_socket = self.cache.find_socket_by_name(next_parent_equip, out_port_name)
                        if out_socket:
                            trace_table.add_row(
                                "", "[dim]->[/dim]", f"[blue]Traversée de {next_parent_name}[/blue]", "(Interne)",
                                "", out_socket.name
                            )
                            current_socket = out_socket # Le prochain point de départ est le port OUT
                        else:
                            current_socket = None # Arrêt si pas de port OUT
                    else:
                        # Si on arrive sur un port OUT, c'est une fin de segment, on passe au suivant
                        current_socket = next_socket

                # Si la destination est un Hub
                elif getattr(next_parent_equip, 'itemtype', None) == 'NetworkEquipment' and 'HB' in next_parent_name.upper():
                    if " IN" in next_socket.name.upper():
                         # Trouver le port OUT du hub (le plus grand numéro)
                        hub_ports = [p.socket for p in next_parent_equip.networkports if hasattr(p, 'socket')]
                        out_socket = max(hub_ports, key=lambda s: int(s.name.split()[-1]))
                        trace_table.add_row(
                            "", "[dim]->[/dim]", f"[blue]Concentration via {next_parent_name}[/blue]", "(Interne)",
                            "", out_socket.name
                        )
                        current_socket = out_socket
                    else: # On sort du hub
                        current_socket = next_socket
                
                else: # Cas standard (PC, Switch non-hub)
                    current_socket = next_socket
            
            # Si le port n'a pas de destination
            else:
                trace_table.add_row(
                    str(step), parent_name, current_socket.name,
                    "[yellow]Non connecté[/yellow]", "", ""
                )
                current_socket = None # Fin de la trace

            step += 1
        
        self.console.print(trace_table)