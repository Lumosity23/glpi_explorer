from src.commands.base_command import BaseCommand
from rich.panel import Panel
from rich.table import Table
from rich import print_json

class DebugCommand(BaseCommand):
    def __init__(self, api_client, console, cache):
        super().__init__(api_client, console, cache)
        self.name = "debug"
        self.description = "Inspecte le cache de topologie."
        self.aliases = ["dbg"]

    def execute(self, args):
        parts = args.split()
        if not parts or parts[0].lower() != 'cache':
            self.console.print(Panel("Usage: debug cache [<type>] [<id>]", title="[red]Erreur[/red]"))
            return

        # 'debug cache' sans arguments
        if len(parts) == 1:
            self._display_cache_summary()
            return
        
        # 'debug cache <type> [<id>]'
        if len(parts) >= 2:
            user_type_alias = parts[1].lower()
            item_id = int(parts[2]) if len(parts) > 2 else None
            
            glpi_itemtype = self.TYPE_ALIASES.get(user_type_alias)
            if not glpi_itemtype:
                self.console.print(Panel(f"Type d'alias inconnu : '{user_type_alias}'", title="[red]Erreur[/red]"))
                return

            if item_id:
                # Mode détail : 'debug cache <type> <id>'
                self._display_item_details(glpi_itemtype, item_id)
            else:
                # Mode liste non implémenté pour l'instant
                self.console.print(Panel(f"La vue liste pour le type '{user_type_alias}' n'est pas encore implémentée.", title="[yellow]Info[/yellow]"))

    def _display_cache_summary(self):
        if not self.cache:
            self.console.print("[red]Le cache n'est pas initialisé.[/red]")
            return

        table = Table(title="Résumé du Cache de Topologie")
        table.add_column("Type d'Objet", style="cyan")
        table.add_column("Nombre d'Éléments", justify="right")
        
        table.add_row("Computers", str(len(self.cache.computers)))
        table.add_row("NetworkEquipments", str(len(self.cache.network_equipments)))
        table.add_row("PassiveDCEquipments", str(len(self.cache.passive_devices)))
        table.add_row("Cables", str(len(self.cache.cables)))
        table.add_row("NetworkPorts", str(len(self.cache.network_ports)))
        table.add_row("Sockets", str(len(self.cache.sockets)))
        
        self.console.print(table)

    def _display_item_details(self, itemtype, item_id):
        # Dictionnaire pour mapper l'itemtype à l'attribut du cache
        cache_map = {
            'Computer': self.cache.computers,
            'NetworkEquipment': self.cache.network_equipments,
            'PassiveDCEquipment': self.cache.passive_devices,
            'Cable': self.cache.cables,
            'NetworkPort': self.cache.network_ports,
            'Glpi\\Socket': self.cache.sockets
        }
        
        target_dict = cache_map.get(itemtype)
        if target_dict is None:
            self.console.print(Panel(f"Le type '{itemtype}' n'est pas géré dans le cache de débogage.", title="[red]Erreur[/red]"))
            return

        item = target_dict.get(item_id)
        if not item:
            self.console.print(Panel(f"Aucun objet de type '{itemtype}' avec l'ID {item_id} trouvé dans le cache.", title="[red]Non Trouvé[/red]"))
            return
            
        self.console.print(f"[bold blue]Détails pour {itemtype} ID {item_id} depuis le cache :[/bold blue]")
        # Utilise vars() pour convertir le SimpleNamespace en dictionnaire pour print_json
        print_json(data=vars(item))
        
        if hasattr(item, 'parent_item') and item.parent_item:
            self.console.print(f"[bold cyan]-> Parent Item:[/bold cyan] {item.parent_item.name} (ID: {item.parent_item.id})")
            
        if hasattr(item, 'connected_to') and item.connected_to:
            connected_socket = item.connected_to
            connected_parent = getattr(connected_socket, 'parent_item', None)
            parent_name = getattr(connected_parent, 'name', 'Parent Inconnu')
            self.console.print(f"[bold green]-> Connected To:[/bold green] Socket '{connected_socket.name}' (ID: {connected_socket.id}) sur l'équipement '{parent_name}'")
