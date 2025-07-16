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
            main_task = progress_bar.add_task("Chargement de la topologie...", total=6)

            self._load_computers(progress_bar, main_task)
            self._load_network_equipments(progress_bar, main_task)
            self._load_passive_devices(progress_bar, main_task)
            self._load_cables(progress_bar, main_task)
            self._load_sockets(progress_bar, main_task)
            self._load_network_ports(progress_bar, main_task)

            final_panel = Panel(
                Align.center(logo_text),
                title="Bienvenue dans GLPI Explorer",
                subtitle="v0.1"
            )
            live.update(final_panel)

    def _load_computers(self, progress, main_task_id):
        progress.update(main_task_id, description="[cyan]Computers...")
        id_list = self.api_client.list_items('Computer', item_range="0-9999", only_id=True)
        if not id_list:
            progress.advance(main_task_id)
            return
        sub_task = progress.add_task("Chargement des détails...", total=len(id_list))
        for item_ref in id_list:
            item_id = item_ref.get('id')
            if item_id:
                details = self.api_client.get_item_details('Computer', item_id)
                if details:
                    details['itemtype'] = 'Computer'
                    self.computers[item_id] = types.SimpleNamespace(**details)
            progress.advance(sub_task)
        progress.remove_task(sub_task)
        progress.advance(main_task_id)

    def _load_network_equipments(self, progress, main_task_id):
        progress.update(main_task_id, description="[cyan]Network Equipments...")
        id_list = self.api_client.list_items('NetworkEquipment', item_range="0-9999", only_id=True)
        if not id_list:
            progress.advance(main_task_id)
            return
        sub_task = progress.add_task("Chargement des détails...", total=len(id_list))
        for item_ref in id_list:
            item_id = item_ref.get('id')
            if item_id:
                details = self.api_client.get_item_details('NetworkEquipment', item_id)
                if details:
                    details['itemtype'] = 'NetworkEquipment'
                    self.network_equipments[item_id] = types.SimpleNamespace(**details)
            progress.advance(sub_task)
        progress.remove_task(sub_task)
        progress.advance(main_task_id)

    def _load_passive_devices(self, progress, main_task_id):
        progress.update(main_task_id, description="[cyan]Passive Devices...")
        id_list = self.api_client.list_items('PassiveDCEquipment', item_range="0-9999", only_id=True)
        if not id_list:
            progress.advance(main_task_id)
            return
        sub_task = progress.add_task("Chargement des détails...", total=len(id_list))
        for item_ref in id_list:
            item_id = item_ref.get('id')
            if item_id:
                details = self.api_client.get_item_details('PassiveDCEquipment', item_id)
                if details:
                    details['itemtype'] = 'PassiveDCEquipment'
                    self.passive_devices[item_id] = types.SimpleNamespace(**details)
            progress.advance(sub_task)
        progress.remove_task(sub_task)
        progress.advance(main_task_id)

    def _load_cables(self, progress, main_task_id):
        progress.update(main_task_id, description="[cyan]Cables...")
        id_list = self.api_client.list_items('Cable', item_range="0-9999", only_id=True)
        if not id_list:
            progress.advance(main_task_id)
            return
        sub_task = progress.add_task("Chargement des détails...", total=len(id_list))
        for item_ref in id_list:
            item_id = item_ref.get('id')
            if item_id:
                details = self.api_client.get_item_details('Cable', item_id)
                if details:
                    details['itemtype'] = 'Cable'
                    self.cables[item_id] = types.SimpleNamespace(**details)
            progress.advance(sub_task)
        progress.remove_task(sub_task)
        progress.advance(main_task_id)

    def _load_sockets(self, progress, main_task_id):
        progress.update(main_task_id, description="[cyan]Sockets...")
        id_list = self.api_client.list_items('Glpi\\Socket', item_range="0-9999", only_id=True)
        if not id_list:
            progress.advance(main_task_id)
            return
        sub_task = progress.add_task("Chargement des détails...", total=len(id_list))
        for item_ref in id_list:
            item_id = item_ref.get('id')
            if item_id:
                details = self.api_client.get_item_details('Glpi\\Socket', item_id)
                if details:
                    details['itemtype'] = 'Glpi\\Socket'
                    self.sockets[item_id] = types.SimpleNamespace(**details)
            progress.advance(sub_task)
        progress.remove_task(sub_task)
        progress.advance(main_task_id)

    def _load_network_ports(self, progress, main_task_id):
        progress.update(main_task_id, description="[cyan]Network Ports...")
        id_list = self.api_client.list_items('NetworkPort', item_range="0-9999", only_id=True)
        if not id_list:
            progress.advance(main_task_id)
            return
        sub_task = progress.add_task("Chargement des détails...", total=len(id_list))
        for item_ref in id_list:
            item_id = item_ref.get('id')
            if item_id:
                details = self.api_client.get_item_details('NetworkPort', item_id)
                if details:
                    details['itemtype'] = 'NetworkPort'
                    self.network_ports[item_id] = types.SimpleNamespace(**details)
            progress.advance(sub_task)
        progress.remove_task(sub_task)
        progress.advance(main_task_id)

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