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

    def __init__(self, api_client, console, cache):
        self.api_client = api_client
        self.console = console
        self.cache = cache


    def get_target_dict(self, glpi_itemtype: str) -> dict:
        if glpi_itemtype == 'Computer': return self.cache.computers
        elif glpi_itemtype == 'NetworkEquipment': return self.cache.network_equipments
        elif glpi_itemtype == 'PassiveDCEquipment': return self.cache.passive_dc_equipments
        elif glpi_itemtype == 'Cable': return self.cache.cables
        elif glpi_itemtype == 'Glpi\\Socket': return self.cache.sockets
        elif glpi_itemtype == 'NetworkPort': return self.cache.network_ports
        # ... ajoutez les autres elif pour tous les types ...
        return None

    def execute(self, args):
        raise NotImplementedError("Subclasses must implement this method")

    def get_help_message(self):
        raise NotImplementedError("Subclasses must provide a help message")

    def _get_item_type(self, user_type_alias: str) -> str:
        return self.TYPE_ALIASES.get(user_type_alias.lower(), user_type_alias)

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
        else:
            table = Table(title=f"Détails de {getattr(details, "name", "N/A")}", expand=True)
            table.add_column("ID")
            table.add_column("Nom")
            table.add_column("Type")
            table.add_column("Statut")
            table.add_column("Localisation")
            table.add_column("Nom du Port", style="cyan")
            table.add_column("Vitesse", style="green")
            table.add_column("Adresse MAC", style="yellow")

            all_ports = getattr(details, "ports", [])

            if not all_ports:
                table.add_row(
                    str(getattr(details, "id", "N/A")),
                    getattr(details, "name", "N/A"),
                    glpi_itemtype,
                    str(getattr(details, "states_id", "N/A")),
                    str(getattr(details, "locations_id", "N/A")),
                    "N/A",
                    "N/A",
                    "N/A",
                )
            else:
                for i, port in enumerate(all_ports):
                    if i == 0:
                        table.add_row(
                            str(getattr(details, "id", "N/A")),
                            getattr(details, "name", "N/A"),
                            glpi_itemtype,
                            str(getattr(details, "states_id", "N/A")),
                            str(getattr(details, "locations_id", "N/A")),
                            getattr(port, "name", "N/A"),
                            f'{getattr(port, "speed", "N/A")} Mbps' if getattr(port, "speed", "N/A") != "N/A" else "N/A",
                            getattr(port, "mac", "N/A"),
                        )
                    else:
                        table.add_row(
                            "", "", "", "", "",
                            getattr(port, "name", "N/A"),
                            f'{getattr(port, "speed", "N/A")} Mbps' if getattr(port, "speed", "N/A") != "N/A" else "N/A",
                            getattr(port, "mac", "N/A"),
                        )
            return table