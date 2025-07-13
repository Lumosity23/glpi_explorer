from src.commands.base_command import BaseCommand
from rich.table import Table
from rich.panel import Panel
from rich.console import Group
from rich.text import Text
from rich import box
from src.api_client import ApiClient

class GetCommand(BaseCommand):
    def get_help_message(self):
        return {
            "description": "Récupère et affiche les détails d'un objet GLPI spécifique ou d'un port.",
            "usage": "get <type> <nom_objet> | get port <nom_port> on <nom_equipement>"
        }

    def execute(self, args):
        if not args:
            self.console.print(Panel("[bold red]Erreur:[/bold red] La commande 'get' nécessite des arguments.\nUsage: get <type> <nom_objet> | get port <nom_port> on <nom_equipement>", title="[red]Utilisation[/red]"))
            return

        parts = args.split(maxsplit=1)
        command_type = parts[0].lower()

        if command_type == "port":
            self._get_port_details(parts[1] if len(parts) > 1 else "")
        else:
            self._get_item_details(args)

    def _get_item_details(self, args):
        try:
            user_type_alias, item_name = args.split(maxsplit=1)
        except ValueError:
            self.console.print(Panel("[bold red]Erreur:[/bold red] Syntaxe incorrecte. Il manque soit le type, soit le nom de l'objet.\nUsage: get <type> <nom_objet>", title="[red]Utilisation[/red]"))
            return

        glpi_itemtype = self.TYPE_ALIASES.get(user_type_alias.lower())
        
        if not glpi_itemtype:
            self.console.print(Panel(f"[bold red]Erreur:[/bold red] Le type '{user_type_alias}' est inconnu.", title="[red]Type Inconnu[/red]"))
            return
        
        with self.console.status(f"Récupération de la liste des '{glpi_itemtype}'..."):
            all_items = self.api_client.list_items(glpi_itemtype, item_range="0-9999")

        if not all_items:
            self.console.print(Panel(f"Aucun objet de type '{user_type_alias}' trouvé dans GLPI.", title="[blue]Information[/blue]", border_style="blue"))
            return

        found_item = None
        for item in all_items:
            if item.get("name", "").lower() == item_name.lower():
                found_item = item
                break
        
        if found_item is None:
            self.console.print(Panel(f"Erreur: Aucun objet de type '{user_type_alias}' nommé '{item_name}' trouvé.", title="[red]Non trouvé[/red]"))
            return

        item_id = found_item.get("id")
        canonical_item_name = found_item.get("name", item_name)

        with self.console.status(f"Récupération des détails de {canonical_item_name}..."):
            details = self.api_client.get_item_details(glpi_itemtype, item_id)
        
        if details:
            display_object = self._render_item_details_to_display_object(details, glpi_itemtype)
            self.console.print(Panel(display_object, title=f"[bold blue]Détails de {canonical_item_name}[/bold blue]"))
        else:
            self.console.print(Panel(f"[bold red]Erreur:[/bold red] Impossible de récupérer les détails pour '{canonical_item_name}'.", title="[red]Erreur[/red]"))

    def _get_port_details(self, args):
        parts = args.lower().split(" on ", 1)
        if len(parts) != 2:
            self.console.print(Panel("[bold red]Erreur:[/bold red] Syntaxe incorrecte pour 'get port'.\nUsage: get port <nom_port> on <nom_equipement>", title="[red]Utilisation[/red]"))
            return
        
        port_name = parts[0].strip().strip('"')
        device_name = parts[1].strip().strip('"')

        if not port_name or not device_name:
            self.console.print(Panel("[bold red]Erreur:[/bold red] Le nom du port ou de l'équipement ne peut pas être vide.\nUsage: get port <nom_port> on <nom_equipement>", title="[red]Utilisation[/red]"))
            return

        with self.console.status(f"Recherche de l'équipement '{device_name}'..."):
            possible_itemtypes = ["Computer", "NetworkEquipment", "Peripheral", "Monitor", "Phone", "Printer"] 
            found_device = None
            device_itemtype = None

            for itemtype_alias in possible_itemtypes:
                glpi_itemtype = self.TYPE_ALIASES.get(itemtype_alias.lower())
                if glpi_itemtype:
                    all_items = self.api_client.list_items(glpi_itemtype, item_range="0-9999")
                    for item in all_items:
                        if item.get("name", "").lower() == device_name.lower():
                            found_device = item
                            device_itemtype = glpi_itemtype
                            break
                if found_device:
                    break
            
            if found_device is None:
                self.console.print(Panel(f"[bold red]Erreur:[/bold red] Aucun équipement nommé '{device_name}' trouvé.", title="[red]Non trouvé[/red]"))
                return

        device_id = found_device.get("id")
        with self.console.status(f"Récupération des détails de l'équipement '{device_name}'..."):
            device_details = self.api_client.get_item_details(device_itemtype, device_id)

        if not device_details:
            self.console.print(Panel(f"[bold red]Erreur:[/bold red] Impossible de récupérer les détails pour l'équipement '{device_name}'.", title="[red]Erreur[/red]"))
            return

        found_port = None
        network_ports_data = device_details.get("_networkports", {})
        for port_list in network_ports_data.values():
            for port in port_list:
                if port.get("name", "").lower() == port_name.lower():
                    found_port = port
                    break
            if found_port:
                break

        if found_port is None:
            self.console.print(Panel(f"[bold red]Erreur:[/bold red] Aucun port nommé '{port_name}' trouvé sur l'équipement '{device_name}'.", title="[red]Non trouvé[/red]"))
            return

        # Table 1: General Port Information
        general_port_info_table = Table(title=f"Informations Générales du Port '{port_name}' sur '{device_name}'", expand=True)
        general_port_info_table.add_column("Propriété")
        general_port_info_table.add_column("Valeur")

        general_port_info_table.add_row("ID du Port", str(found_port.get("id", "N/A")))
        general_port_info_table.add_row("Nom du Port", found_port.get("name", "N/A"))
        general_port_info_table.add_row("Type de Port", str(found_port.get("networkporttypes_id", "N/A")))
        general_port_info_table.add_row("MAC", found_port.get("mac", "N/A"))
        general_port_info_table.add_row("Vitesse", f"{found_port.get('speed', 'N/A')} Mbps")
        general_port_info_table.add_row("Statut", str(found_port.get("states_id", "N/A")))

        # Table 2: Detailed Connection Information
        connection_info_table = Table(title="Informations de Connexion Détaillées", expand=True)
        connection_info_table.add_column("Propriété")
        connection_info_table.add_column("Valeur")

        # Find the Glpi\\Socket associated with this NetworkPort
        associated_socket = None
        with self.console.status(f"Recherche du socket associé au port '{port_name}'..."):
            all_sockets = self.api_client.list_items("Glpi\\Socket", item_range="0-9999")
            for socket in all_sockets:
                if str(socket.get("networkports_id")) == str(found_port.get("id")) and str(socket.get("items_id")) == str(device_id):
                    associated_socket = socket
                    break

        if associated_socket:
            connection_info_table.add_row("Socket Associé (ID)", str(associated_socket.get("id")))
            connection_info_table.add_row("Socket Associé (Nom)", associated_socket.get("name", "N/A"))

            cable_info = None
            with self.console.status(f"Récupération du câble pour le socket '{associated_socket.get('name')}'..."):
                cable_info = self.api_client.get_cable_on_socket(associated_socket.get("id"))

            if cable_info:
                connection_info_table.add_row("Câble Connecté", cable_info.get("name", "N/A"))

                socket_ids_from_links = []
                for link in cable_info.get("links", []):
                    if link.get("rel") == "Glpi\\Socket":
                        try:
                            socket_id = link["href"].split("/")[-1]
                            socket_ids_from_links.append(socket_id)
                        except IndexError:
                            self.console.print(f"[DEBUG] Could not extract socket ID from href: {link['href']}")
                
                self.console.print(f"[DEBUG] Found socket IDs in cable: {socket_ids_from_links}")

                socket_a_details = None
                socket_b_details = None

                if len(socket_ids_from_links) >= 1:
                    socket_a_details = self.api_client.get_socket_details(socket_ids_from_links[0])
                if len(socket_ids_from_links) >= 2:
                    socket_b_details = self.api_client.get_socket_details(socket_ids_from_links[1])

                # Display Socket A details
                if socket_a_details:
                    socket_a_name = socket_a_details.get("name", "N/A")
                    socket_a_type_id = socket_a_details.get("socketmodels_id", "N/A")
                    socket_a_networkport_id = socket_a_details.get("networkports_id", "N/A")
                    socket_a_parent_itemtype = socket_a_details.get("itemtype", "N/A")
                    socket_a_parent_item_id = socket_a_details.get("items_id", "N/A")

                    socket_a_type_name = "N/A"
                    if socket_a_type_id != "N/A":
                        socket_a_type_details = self.api_client.get_item_details("Glpi\\SocketModel", socket_a_type_id)
                        if socket_a_type_details:
                            socket_a_type_name = socket_a_type_details.get("name", "N/A")

                    connection_info_table.add_row("Socket A (Câble)", f"{socket_a_name} (Type: {socket_a_type_name}, Port ID: {socket_a_networkport_id}, Device: {socket_a_parent_itemtype}/{socket_a_parent_item_id})")
                else:
                    connection_info_table.add_row("Socket A (Câble)", "Détails non disponibles")

                # Display Socket B details
                if socket_b_details:
                    socket_b_name = socket_b_details.get("name", "N/A")
                    socket_b_type_id = socket_b_details.get("socketmodels_id", "N/A")
                    socket_b_networkport_id = socket_b_details.get("networkports_id", "N/A")
                    socket_b_parent_itemtype = socket_b_details.get("itemtype", "N/A")
                    socket_b_parent_item_id = socket_b_details.get("items_id", "N/A")

                    socket_b_type_name = "N/A"
                    if socket_b_type_id != "N/A":
                        socket_b_type_details = self.api_client.get_item_details("Glpi\\SocketModel", socket_b_type_id)
                        if socket_b_type_details:
                            socket_b_type_name = socket_b_type_details.get("name", "N/A")

                    connection_info_table.add_row("Socket B (Câble)", f"{socket_b_name} (Type: {socket_b_type_name}, Port ID: {socket_b_networkport_id}, Device: {socket_b_parent_itemtype}/{socket_b_parent_item_id})")
                else:
                    connection_info_table.add_row("Socket B (Câble)", "Détails non disponibles")

                # Determine the other end of the cable based on the current port's ID
                other_socket_details = None
                if socket_a_details and str(socket_a_details.get("networkports_id")) == str(found_port.get("id")):
                    other_socket_details = socket_b_details
                elif socket_b_details and str(socket_b_details.get("networkports_id")) == str(found_port.get("id")):
                    other_socket_details = socket_a_details
                
                if other_socket_details:
                    other_device_itemtype = other_socket_details.get("itemtype")
                    other_device_item_id = other_socket_details.get("items_id")
                    other_networkport_id = other_socket_details.get("networkports_id")

                    if other_device_itemtype and other_device_item_id:
                        with self.console.status(f"Récupération des détails de l'équipement distant (ID: {other_device_item_id}, Type: {other_device_itemtype})..."):
                            other_device_details = self.api_client.get_item_details(other_device_itemtype, other_device_item_id)
                            if other_device_details:
                                other_device_name = other_device_details.get("name", "Nom inconnu")
                                connection_info_table.add_row("Connecté à (autre équipement)", f"{other_device_name} (Type: {other_device_itemtype}, ID: {other_device_item_id})")
                                connection_info_table.add_row("Port distant", f"{other_socket_details.get('name', 'Nom inconnu')} (ID: {other_networkport_id})")
                            else:
                                connection_info_table.add_row("Connecté à (autre équipement)", f"ID: {other_device_item_id}, Type: {other_device_itemtype} (Détails non récupérables)")
                                connection_info_table.add_row("Port distant", f"ID: {other_networkport_id} (Détails non récupérables)")
                    else:
                        connection_info_table.add_row("Connecté à (autre équipement)", "Non spécifié")
                        connection_info_table.add_row("Port distant", "Non spécifié")
                else:
                    connection_info_table.add_row("Connecté à (autre équipement)", "Non spécifié")
                    connection_info_table.add_row("Port distant", "Non spécifié")
            else:
                connection_info_table.add_row("Câble Connecté", "Aucun")
                connection_info_table.add_row("Socket A (Câble)", "N/A")
                connection_info_table.add_row("Socket B (Câble)", "N/A")
                connection_info_table.add_row("Connecté à (autre équipement)", "N/A")
                connection_info_table.add_row("Port distant", "N/A")
        else:
            connection_info_table.add_row("Socket Associé", "Aucun trouvé pour ce port")
            connection_info_table.add_row("Câble Connecté", "Aucun")
            connection_info_table.add_row("Socket A (Câble)", "N/A")
            connection_info_table.add_row("Socket B (Câble)", "N/A")
            connection_info_table.add_row("Connecté à (autre équipement)", "N/A")
            connection_info_table.add_row("Port distant", "N/A")

        render_group = Group(general_port_info_table, Text(""), connection_info_table)
        self.console.print(Panel(render_group))