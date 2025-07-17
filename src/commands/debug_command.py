from src.commands.base_command import BaseCommand
from rich.panel import Panel
from rich.table import Table
from rich import print_json
import types

class DebugCommand(BaseCommand):
    def __init__(self, api_client, console, cache):
        super().__init__(api_client, console, cache)
        self.name = "debug"
        self.description = "Inspecte le cache de topologie."
        self.aliases = ["dbg"]

    def get_help_message(self):
        return {
            "description": self.description,
            "usage": "debug cache [<type>] [<id>|<nom>]"
        }

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
            identifier = parts[2] if len(parts) > 2 else None
            
            glpi_itemtype = self.TYPE_ALIASES.get(user_type_alias)
            if not glpi_itemtype:
                self.console.print(Panel(f"Type d'alias inconnu : '{user_type_alias}'", title="[red]Erreur[/red]"))
                return

            if identifier:
                # Essayer de convertir en ID entier
                try:
                    item_id = int(identifier)
                    self._display_item_details(glpi_itemtype, item_id)
                except ValueError:
                    # Si ce n'est pas un ID, le traiter comme un nom
                    self._display_item_details_by_name(glpi_itemtype, identifier)
            else:
                # Mode liste
                self._display_item_list(glpi_itemtype)

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
        
        table.add_row("Sockets", str(len(self.cache.sockets)))
        table.add_row("NetworkPorts", str(len(self.cache.network_ports)))
        
        self.console.print(table)

    def _display_item_list(self, itemtype):
        cache_map = {
            'Computer': self.cache.computers,
            'NetworkEquipment': self.cache.network_equipments,
            'PassiveDCEquipment': self.cache.passive_devices,
            'Cable': self.cache.cables,
            'Glpi\\Socket': self.cache.sockets,
            'NetworkPort': self.cache.network_ports
        }

        target_dict = cache_map.get(itemtype)
        if target_dict is None:
            self.console.print(Panel(f"Le type '{itemtype}' n'est pas géré pour la liste de débogage.", title="[red]Erreur[/red]"))
            return

        if not target_dict:
            self.console.print(Panel(f"Aucun objet de type '{itemtype}' trouvé dans le cache.", title="[yellow]Info[/yellow]"))
            return

        table = Table(title=f"Liste des {itemtype}s", show_lines=True)
        table.add_column("ID", justify="right", style="cyan", no_wrap=True)
        table.add_column("Nom", style="magenta")
        table.add_column("Parent ID", style="green")
        table.add_column("Parent Type", style="blue")

        for item_id, item in target_dict.items():
            parent_id = getattr(item, 'items_id', 'N/A')
            parent_type = getattr(item, 'itemtype', 'N/A')
            table.add_row(str(item_id), getattr(item, 'name', 'N/A'), str(parent_id), parent_type)

        self.console.print(table)

    def _display_item_details(self, itemtype, item_id):
        # Dictionnaire pour mapper l'itemtype à l'attribut du cache
        cache_map = {
            'Computer': self.cache.computers,
            'NetworkEquipment': self.cache.network_equipments,
            'PassiveDCEquipment': self.cache.passive_devices,
            'Cable': self.cache.cables,
            
            'Glpi\\Socket': self.cache.sockets,
            'NetworkPort': self.cache.network_ports
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
        
        # Créer une table pour afficher les attributs de l'objet
        details_table = Table(title="Attributs de l'Objet", box=None, show_header=False)
        details_table.add_column("Attribut", style="cyan")
        details_table.add_column("Valeur")

        # Itérer sur les attributs de l'objet SimpleNamespace
        for attr, value in vars(item).items():
            if attr == 'networkports' and isinstance(value, list):
                display_value = f"Liste de {len(value)} NetworkPort(s)"
            elif isinstance(value, types.SimpleNamespace):
                display_value = f"Objet {value.__class__.__name__} (ID: {getattr(value, 'id', 'N/A')})"
            elif isinstance(value, list) and value and isinstance(value[0], types.SimpleNamespace):
                 display_value = f"Liste de {len(value)} objet(s) {value[0].__class__.__name__}"
            else:
                display_value = str(value)
            
            details_table.add_row(attr, display_value)
            
        self.console.print(details_table)

    def _display_item_details_by_name(self, itemtype, item_name):
        cache_map = {
            'Computer': self.cache.computers,
            'NetworkEquipment': self.cache.network_equipments,
            'PassiveDCEquipment': self.cache.passive_devices,
            'Cable': self.cache.cables,
            'Glpi\\Socket': self.cache.sockets,
            'NetworkPort': self.cache.network_ports
        }

        target_dict = cache_map.get(itemtype)
        if target_dict is None:
            self.console.print(Panel(f"Le type '{itemtype}' n'est pas géré pour la recherche par nom.", title="[red]Erreur[/red]"))
            return

        found_item = None
        for item in target_dict.values():
            if getattr(item, 'name', '').lower() == item_name.lower():
                found_item = item
                break

        if found_item:
            self._display_item_details(itemtype, found_item.id)
        else:
            self.console.print(Panel(f"Aucun objet de type '{itemtype}' avec le nom '{item_name}' trouvé dans le cache.", title="[red]Non Trouvé[/red]"))
