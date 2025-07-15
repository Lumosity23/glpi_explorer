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