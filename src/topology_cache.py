import pickle
import types
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.panel import Panel
from rich.console import Console, Group
from rich.text import Text
from rich.live import Live
from rich.align import Align

class TopologyCache:
    def __init__(self, api_client, cache_file='topology_cache.pkl'):
        self.api_client = api_client
        self.cache_file = cache_file
        self.computers = {}
        self.network_equipments = {}
        self.passive_devices = {}
        self.cables = {}
        self.sockets = {}
        self.network_ports = {}

    def load_from_api(self, console):
        self.console = console

        logo = """
         ██████╗ ██╗     ██████╗ ██╗      ███████╗██╗  ██╗██████╗ ██╗      ██████╗ ██████╗ ███████╗██████╗ 
        ██╔════╝ ██║     ██╔══██╗██║      ██╔════╝╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██╔══██╗██╔════╝██╔══██╗
        ██║  ███╗██║     ██████╔╝██║█████╗█████╗   ╚███╔╝ ██████╔╝██║     ██║   ██║██████╔╝█████╗  ██████╔╝
        ██║   ██║██║     ██╔═══╝ ██║╚════╝██╔══╝   ██╔██╗ ██╔═══╝ ██║     ██║   ██║██╔══██╗██╔══╝  ██╔══██╗
        ╚██████╔╝███████╗██║     ██║      ███████╗██╔╝ ██╗██║     ███████╗╚██████╔╝██║  ██║███████╗██║  ██║
         ╚═════╝ ╚══════╝╚═╝     ╚═╝      ╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
        """

        item_types_to_load = {
            "Computer": self.computers,
            "NetworkEquipment": self.network_equipments,
            "PassiveDCEquipment": self.passive_devices,
            "Glpi\\Socket": self.sockets,
            "Cable": self.cables,
            "NetworkPort": self.network_ports,
        }

        id_lists = {}
        total_items = 0
        for item_type in item_types_to_load.keys():
            id_list = self.api_client.list_items(item_type, item_range="0-9999", only_id=True)
            id_lists[item_type] = id_list
            total_items += len(id_list)

        logo_text = Text(logo, justify="center", style="bold blue")

        progress_bar = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        )
        
        loading_group = Group(logo_text, progress_bar)
        panel = Panel(Align.center(loading_group))

        with Live(panel, console=console, redirect_stderr=False) as live:
            task = progress_bar.add_task("Chargement de la topologie...", total=total_items)
            for item_type, target_dict in item_types_to_load.items():
                id_list = id_lists[item_type]
                for i, item_ref in enumerate(id_list):
                    item_id = item_ref.get('id')
                    if item_id:
                        details = self.api_client.get_item_details(item_type, item_id)
                        if details:
                            details['itemtype'] = item_type
                            target_dict[item_id] = types.SimpleNamespace(**details)
                    progress_bar.update(task, advance=1, description=f"Chargement {item_type}: {i+1}/{len(id_list)}")
            
            final_panel = Panel(
                Align.center(logo_text),
                title="Bienvenue dans GLPI Explorer",
                subtitle="v0.1"
            )
            live.update(final_panel)

        self._link_topology()

    def _link_topology(self):
        all_equipment = {**self.computers, **self.network_equipments, **self.passive_devices}

        # Pass 1: Link NetworkPorts to their parent equipment and Sockets
        for port in self.network_ports.values():
            parent_id = port.items_id
            parent_type = port.itemtype
            if parent_type == 'Computer' and parent_id in self.computers:
                port.parent_item = self.computers[parent_id]
            elif parent_type == 'NetworkEquipment' and parent_id in self.network_equipments:
                port.parent_item = self.network_equipments[parent_id]
            elif parent_type == 'PassiveDCEquipment' and parent_id in self.passive_devices:
                port.parent_item = self.passive_devices[parent_id]

            if hasattr(port, 'sockets_id') and port.sockets_id in self.sockets:
                socket = self.sockets[port.sockets_id]
                port.socket = socket
                socket.networkport = port
                socket.parent_item = port.parent_item

        # Pass 2: Link Sockets to each other via Cables
        for cable in self.cables.values():
            socket_ids = []
            for link in getattr(cable, 'links', []):
                if link.get('rel') == 'Glpi\\Socket':
                    try:
                        socket_id = int(link['href'].split('/')[-1])
                        socket_ids.append(socket_id)
                    except (ValueError, IndexError):
                        continue
            
            if len(socket_ids) == 2:
                socket_a = self.sockets.get(socket_ids[0])
                socket_b = self.sockets.get(socket_ids[1])
                if socket_a and socket_b:
                    socket_a.connected_to = socket_b
                    socket_b.connected_to = socket_a
                    socket_a.via_cable = cable
                    socket_b.via_cable = cable

    def find_socket_by_name(self, parent_equip, socket_name):
        """Trouve un socket par son nom sur un équipement spécifique."""
        for port in getattr(parent_equip, '_networkports', {}).get('NetworkPortEthernet', []):
            socket = getattr(self.network_ports.get(port['id']), 'socket', None)
            if socket and getattr(socket, 'name', '').lower() == socket_name.lower():
                return socket
        return None

    def save_to_disk(self):
        with open(self.cache_file, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load_from_disk(cache_file='topology_cache.pkl'):
        try:
            with open(cache_file, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return None
