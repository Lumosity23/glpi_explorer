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
        table.add_row("PassiveDCEquipments", str(len(self.cache.passive_dc_equipments)))
        table.add_row("Cables", str(len(self.cache.cables)))
        
        table.add_row("Sockets", str(len(self.cache.sockets)))
        
        self.console.print(table)

    def _display_item_details(self, itemtype, item_id):
        # Dictionnaire pour mapper l'itemtype à l'attribut du cache
        cache_map = {
            'Computer': self.cache.computers,
            'NetworkEquipment': self.cache.network_equipments,
            'PassiveDCEquipment': self.cache.passive_dc_equipments,
            'Cable': self.cache.cables,
            
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
        
        # Créer une table pour afficher les attributs de l'objet
        details_table = Table(title="Attributs de l'Objet", box=None, show_header=False)
        details_table.add_column("Attribut", style="cyan")
        details_table.add_column("Valeur")

        # Itérer sur les attributs de l'objet SimpleNamespace
        for attr, value in vars(item).items():
            # Afficher des représentations simples pour les objets complexes pour éviter les erreurs
            if isinstance(value, types.SimpleNamespace):
                display_value = f"Objet {value.__class__.__name__} (ID: {getattr(value, 'id', 'N/A')})"
            elif isinstance(value, list) and value and isinstance(value[0], types.SimpleNamespace):
                 display_value = f"Liste de {len(value)} objet(s) {value[0].__class__.__name__}"
            else:
                display_value = str(value)
            
            details_table.add_row(attr, display_value)
            
        self.console.print(details_table)
