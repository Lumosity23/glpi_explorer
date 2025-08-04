import os
import types
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.console import Group
from rich import box

from src.api_client import ApiClient
from src.config_manager import ConfigManager

class BaseCommand:
    TYPE_ALIASES = {
        'computer': 'Computer', 'pc': 'Computer',
        'monitor': 'Monitor', 'screen': 'Monitor',
        'networkequipment': 'NetworkEquipment', 'network': 'NetworkEquipment',
        'switch': 'NetworkEquipment', 'sw': 'NetworkEquipment',
        'hub': 'NetworkEquipment', 'hb': 'NetworkEquipment',
        'peripheral': 'Peripheral',
        'phone': 'Phone',
        'printer': 'Printer',
        'software': 'Software',
        'ticket': 'Ticket',
        'user': 'User',
        'patchpanel': 'PassiveDCEquipment', 'patch': 'PassiveDCEquipment', 'pp': 'PassiveDCEquipment',
        'walloutlet': 'PassiveDCEquipment', 'wo': 'PassiveDCEquipment',
        'cable': 'Cable', 'cb': 'Cable',
        'socket': 'Glpi\\Socket', 'so': 'Glpi\\Socket',
        'networkport': 'NetworkPort', 'np': 'NetworkPort',
    }

    def __init__(self, api_client, console, cache, shared_state):
        self.api_client = api_client
        self.console = console
        self.cache = cache
        self.shared_state = shared_state


    def get_target_dict(self, glpi_itemtype: str) -> dict:
        if glpi_itemtype == 'Computer': return self.cache.computers
        elif glpi_itemtype == 'NetworkEquipment': return self.cache.network_equipments
        elif glpi_itemtype == 'PassiveDCEquipment': return self.cache.passive_devices
        elif glpi_itemtype == 'Cable': return self.cache.cables
        elif glpi_itemtype == 'Glpi\\Socket': return self.cache.sockets
        elif glpi_itemtype == 'NetworkPort': return self.cache.network_ports
        # ... ajoutez les autres elif pour tous les types ...
        return None

    def execute(self, args):
        raise NotImplementedError("Subclasses must implement this method")

    def get_help_message(self):
        raise NotImplementedError("Subclasses must provide a help message")

    def get_item_type_from_alias(self, alias: str) -> str:
        return self.TYPE_ALIASES.get(alias.lower())

    def _get_color_for_string(self, text: str) -> str:
        """Generates a consistent color for a given string."""
        if not text or text == "N/A":
            return "white"
        # Simple hash-based color selection from a predefined list
        colors = [
            "bright_red", "bright_green", "bright_yellow", "bright_blue", 
            "bright_magenta", "bright_cyan", "red", "green", "yellow", "blue",
            "magenta", "cyan"
        ]
        return colors[abs(hash(text)) % len(colors)]

    def _display_error(self, message: str):
        self.console.print(Panel(Text(message, style="bold red"), title="[red]Erreur[/red]"))

    def _display_info(self, message: str):
        self.console.print(Panel(Text(message, style="blue"), title="[blue]Information[/blue]"))

    def _display_success(self, message: str):
        self.console.print(Panel(Text(message, style="bold green"), title="[green]Succès[/green]"))

    def _display_warning(self, message: str):
        self.console.print(Panel(Text(message, style="bold yellow"), title="[yellow]Avertissement[/yellow]"))

    def _display_json(self, data):
        self.console.print(Panel(self.console.print_json(data=data), title="[cyan]Détails JSON[/cyan]"))

    def _render_item_details_to_display_object(self, details: object, glpi_itemtype: str):
        """
        Renders item details into a rich.Table or a rich.Group of Panels (for cables).
        This method is designed to be reusable by commands like 'get' and 'compare'.
        """
        if glpi_itemtype == "Cable":
            general_info_table = Table(title="Informations Générales du Câble", expand=True, box=box.MINIMAL)
            general_info_table.add_column("ID")
            general_info_table.add_column("Nom")
            general_info_table.add_column("Type")
            general_info_table.add_column("Type Câble")

            general_info_table.add_row(
                str(getattr(details, "id", "N/A")),
                getattr(details, "name", "N/A"),
                glpi_itemtype,
                str(getattr(details, "cabletypes_id", "N/A")),
            )

            endpoints_table = Table(title="Points de Connexion", expand=True, box=box.MINIMAL)
            endpoints_table.add_column("Endpoint")
            endpoints_table.add_column("Type")
            endpoints_table.add_column("Socket")

            socket_a = str(getattr(details, "sockets_id_endpoint_a", "N/A")).replace("(&nbsp;)", "").strip()
            socket_b = str(getattr(details, "sockets_id_endpoint_b", "N/A")).replace("(&nbsp;)", "").strip()

            endpoints_table.add_row(
                "A",
                str(getattr(details, "itemtype_endpoint_a", "N/A")),
                socket_a,
            )
            endpoints_table.add_row(
                "B",
                str(getattr(details, "itemtype_endpoint_b", "N/A")),
                socket_b,
            )
            
            return Group(
                Panel(general_info_table, title=f"[bold blue]Détails du Câble {getattr(details, 'name', 'N/A')}[/bold blue]", box=box.MINIMAL),
                Panel(endpoints_table, title="[bold blue]Points de Connexion[/bold blue]", box=box.MINIMAL)
            )
        else: # Pour tous les équipements non-câbles
            table = Table(title=f"Détails de {getattr(details, 'name', 'N/A')}", expand=True)
            table.add_column("ID")
            table.add_column("Nom")
            table.add_column("Type")
            table.add_column("Statut")
            table.add_column("Localisation")
            table.add_column("Nom du Port", style="cyan")
            table.add_column("Vitesse", style="green")
            table.add_column("Adresse MAC", style="yellow")

            # --- DÉBUT DE LA CORRECTION DE LA LOGIQUE DES PORTS ---
            all_ports = []
            raw_ports_data = getattr(details, "_networkports", {})
            if raw_ports_data:
                for port_list in raw_ports_data.values():
                    all_ports.extend(port_list)
            # --- FIN DE LA CORRECTION ---
            
            # --- DÉBUT DE LA CORRECTION DE LA LOCALISATION ET DU STATUT ---
            location_id = getattr(details, "locations_id", "N/A")
            location_name = "N/A"
            if isinstance(location_id, int) and self.cache.locations.get(location_id):
                location_name = self.cache.locations[location_id].name
            elif location_id != "N/A":
                location_name = str(location_id)

            state_id = getattr(details, "states_id", "N/A")
            state_name = "N/A"
            if isinstance(state_id, int) and hasattr(self.cache, 'states') and self.cache.states.get(state_id):
                state_name = self.cache.states[state_id].name
            elif state_id != "N/A":
                state_name = str(state_id)

            type_color = self._get_color_for_string(glpi_itemtype)
            location_color = self._get_color_for_string(location_name)
            # --- FIN DE LA CORRECTION ---

            if not all_ports:
                table.add_row(
                    str(getattr(details, "id", "N/A")),
                    getattr(details, "name", "N/A"),
                    f"[{type_color}]{glpi_itemtype}[/]",
                    state_name,
                    f"[{location_color}]{location_name}[/]",
                    "N/A", "N/A", "N/A",
                )
            else:
                for i, port_data in enumerate(all_ports):
                    port = types.SimpleNamespace(**port_data) # Convertir le dict en objet
                    if i == 0:
                        table.add_row(
                            str(getattr(details, "id", "N/A")),
                            getattr(details, "name", "N/A"),
                            f"[{type_color}]{glpi_itemtype}[/]",
                            state_name,
                            f"[{location_color}]{location_name}[/]",
                            getattr(port, "name", "N/A"),
                            f'{getattr(port, "speed", "N/A")} Mbps',
                            getattr(port, "mac", "N/A"),
                        )
                    else:
                        table.add_row(
                            "", "", "", "", "",
                            getattr(port, "name", "N/A"),
                            f'{getattr(port, "speed", "N/A")} Mbps',
                            getattr(port, "mac", "N/A"),
                        )
            return table