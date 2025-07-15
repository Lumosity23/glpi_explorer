import pickle
import types
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

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
        progress_columns = [
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        ]
        with Progress(*progress_columns, console=console) as progress:
            main_task = progress.add_task("Chargement de la topologie...", total=6)

            self._load_computers(progress, main_task)
            self._load_network_equipments(progress, main_task)
            self._load_passive_devices(progress, main_task)
            self._load_sockets(progress, main_task)
            self._load_cables(progress, main_task)
            self._load_network_ports(progress, main_task)

        self._link_topology()

    def _load_computers(self, progress, task_id):
        progress.update(task_id, description="[cyan]Computers...")
        id_list = self.api_client.list_items('Computer', item_range="0-9999", only_id=True)
        if not id_list:
            progress.advance(task_id)
            return

        sub_task = progress.add_task("", total=len(id_list), parent=task_id)
        for item_ref in id_list:
            item_id = item_ref.get('id')
            if item_id:
                details = self.api_client.get_item_details('Computer', item_id)
                if details:
                    details['itemtype'] = 'Computer'
                    self.computers[item_id] = types.SimpleNamespace(**details)
            progress.advance(sub_task)
        progress.advance(task_id)

    def _load_network_equipments(self, progress, task_id):
        progress.update(task_id, description="[cyan]NetworkEquipments...")
        id_list = self.api_client.list_items('NetworkEquipment', item_range="0-9999", only_id=True)
        if not id_list:
            progress.advance(task_id)
            return

        sub_task = progress.add_task("", total=len(id_list), parent=task_id)
        for item_ref in id_list:
            item_id = item_ref.get('id')
            if item_id:
                details = self.api_client.get_item_details('NetworkEquipment', item_id)
                if details:
                    details['itemtype'] = 'NetworkEquipment'
                    self.network_equipments[item_id] = types.SimpleNamespace(**details)
            progress.advance(sub_task)
        progress.advance(task_id)

    def _load_passive_devices(self, progress, task_id):
        progress.update(task_id, description="[cyan]PassiveDCEquipments...")
        id_list = self.api_client.list_items('PassiveDCEquipment', item_range="0-9999", only_id=True)
        if not id_list:
            progress.advance(task_id)
            return

        sub_task = progress.add_task("", total=len(id_list), parent=task_id)
        for item_ref in id_list:
            item_id = item_ref.get('id')
            if item_id:
                details = self.api_client.get_item_details('PassiveDCEquipment', item_id)
                if details:
                    details['itemtype'] = 'PassiveDCEquipment'
                    self.passive_devices[item_id] = types.SimpleNamespace(**details)
            progress.advance(sub_task)
        progress.advance(task_id)

    def _load_sockets(self, progress, task_id):
        progress.update(task_id, description="[cyan]Sockets...")
        id_list = self.api_client.list_items('Glpi\\Socket', item_range="0-9999", only_id=True)
        if not id_list:
            progress.advance(task_id)
            return

        sub_task = progress.add_task("", total=len(id_list), parent=task_id)
        for item_ref in id_list:
            item_id = item_ref.get('id')
            if item_id:
                details = self.api_client.get_item_details('Glpi\\Socket', item_id)
                if details:
                    details['itemtype'] = 'Glpi\\Socket'
                    self.sockets[item_id] = types.SimpleNamespace(**details)
            progress.advance(sub_task)
        progress.advance(task_id)

    def _load_cables(self, progress, task_id):
        progress.update(task_id, description="[cyan]Cables...")
        id_list = self.api_client.list_items('Cable', item_range="0-9999", only_id=True)
        if not id_list:
            progress.advance(task_id)
            return

        sub_task = progress.add_task("", total=len(id_list), parent=task_id)
        for item_ref in id_list:
            item_id = item_ref.get('id')
            if item_id:
                details = self.api_client.get_item_details('Cable', item_id)
                if details:
                    details['itemtype'] = 'Cable'
                    self.cables[item_id] = types.SimpleNamespace(**details)
            progress.advance(sub_task)
        progress.advance(task_id)

    def _load_network_ports(self, progress, task_id):
        progress.update(task_id, description="[cyan]NetworkPorts...")
        id_list = self.api_client.list_items('NetworkPort', item_range="0-9999", only_id=True)
        if not id_list:
            progress.advance(task_id)
            return

        sub_task = progress.add_task("", total=len(id_list), parent=task_id)
        for item_ref in id_list:
            item_id = item_ref.get('id')
            if item_id:
                details = self.api_client.get_item_details('NetworkPort', item_id)
                if details:
                    details['itemtype'] = 'NetworkPort'
                    self.network_ports[item_id] = types.SimpleNamespace(**details)
            progress.advance(sub_task)
        progress.advance(task_id)

    def _link_topology(self):
        # Lier les Sockets via les Câbles
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
