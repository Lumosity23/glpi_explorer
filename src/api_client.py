# src/api_client.py
import glpi_api
from rich.console import Console

class ApiClient:
    def __init__(self, config):
        self.config = config
        self.glpi = None
        self.console = Console()

    def connect(self):
        try:
            self.glpi = glpi_api.GLPI(
                url=self.config['url'],
                apptoken=self.config['app_token'],
                auth=self.config['user_token']
            )
            # La connexion est implicite, on fait un petit appel pour la valider
            self.glpi.get_my_profiles() 
            return True
        except glpi_api.GLPIError as err:
            self.console.log(f"[bold red]Erreur de connexion GLPI: {err}[/bold red]")
            return False

    def close_session(self):
        if self.glpi:
            try:
                self.glpi.kill_session()
            except glpi_api.GLPIError:
                pass # La session est peut-être déjà morte, on ignore

    def list_items(self, itemtype, item_range="0-9999", only_id=False):
        """Récupère une liste d'items. 'only_id' n'est plus pertinent de la même manière."""
        try:
            # get_all_items gère la pagination, mais pour le cache on prend tout
            # Note : il faudra peut-être gérer la pagination manuellement si get_all_items a une limite
            return self.glpi.get_all_items(itemtype, range=item_range)
        except glpi_api.GLPIError as err:
            self.console.log(f"[bold red]Erreur lors du listing de {itemtype}: {err}[/bold red]")
            return []

    def get_item_details(self, itemtype, item_id):
        """Récupère les détails complets d'un item."""
        try:
            # La bibliothèque gère 'with_networkports' comme des kwargs
            return self.glpi.get_item(itemtype, item_id, with_networkports=True)
        except glpi_api.GLPIError as err:
            self.console.log(f"[bold red]Erreur lors de la récupération de {itemtype}/{item_id}: {err}[/bold red]")
            return None

    def create_items(self, itemtype, data_list):
        """Crée un ou plusieurs items."""
        try:
            # La méthode add prend des dictionnaires en *args
            return self.glpi.add(itemtype, *data_list)
        except glpi_api.GLPIError as err:
            self.console.log(f"[bold red]Erreur lors de la création de {itemtype}: {err}[/bold red]")
            return None

    def create_item(self, itemtype, data):
        """Crée un seul item."""
        return self.create_items(itemtype, [data])

    def update_item(self, itemtype, item_id, data):
        """Met à jour un item."""
        try:
            # La méthode update attend l'id dans le dictionnaire
            data_with_id = {'id': item_id, **data}
            return self.glpi.update(itemtype, data_with_id)
        except glpi_api.GLPIError as err:
            self.console.log(f"[bold red]Erreur lors de la mise à jour de {itemtype}/{item_id}: {err}[/bold red]")
            return None