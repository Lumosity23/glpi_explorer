import requests
import json

class ApiClient:
    def __init__(self, config):
        self.config = config
        self.base_url = config.get("url")
        self.app_token = config.get("app_token")
        self.user_token = config.get("user_token")
        self.session_token = None

    def connect(self):
        headers = {
            "Authorization": f"user_token {self.user_token}",
            "App-Token": self.app_token,
            "Content-Type": "application/json"
        }
        try:
            response = requests.get(f"{self.base_url}/initSession", headers=headers)
            response.raise_for_status()
            session_token = response.json().get("session_token")
            if session_token:
                self.session_token = session_token
                return True
            return False
        except requests.exceptions.RequestException as e:
            print(f"Erreur de connexion: {e}")
            return False

    def close_session(self):
        if not self.session_token:
            return
        headers = {
            "Session-Token": self.session_token,
            "App-Token": self.app_token,
        }
        try:
            requests.get(f"{self.base_url}/killSession", headers=headers)
        except requests.exceptions.RequestException as e:
            self.console.print(f"[red]Erreur lors de la déconnexion: {e}[/red]")

    def get_sub_items(self, full_href):
        """Fait une requête GET sur une URL complète fournie par un lien HATEOAS."""
        if not self.session_token:
            return []
        headers = {
            "Session-Token": self.session_token,
            "App-Token": self.app_token
        }
        try:
            response = requests.get(full_href, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return []

    def get_item_details(self, itemtype, item_id):
        if not self.session_token:
            return None
        headers = {
            "Session-Token": self.session_token,
            "App-Token": self.app_token,
            "Content-Type": "application/json"
        }
        try:
            params = {
                "expand_dropdowns": "true",
            }
            # Only request network port information for relevant item types
            if itemtype in ["Computer", "NetworkEquipment", "Peripheral", "Phone", "Printer"]:
                params["with_networkports"] = "true"

            response = requests.get(f"{self.base_url}/{itemtype}/{item_id}", headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération des détails: {e}")
            return None





    def list_items(self, itemtype, item_range="0-9999", only_id=True):
        if not self.session_token:
            return []

        headers = {
            "Session-Token": self.session_token,
            "App-Token": self.app_token,
            "Content-Type": "application/json"
        }

        params = {
            "range": item_range,
            "expand_dropdowns": "true",
            "only_id": "true" if only_id else "false"
        }
        try:
            response = requests.get(f"{self.base_url}/{itemtype}/", headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération de la liste: {e}")
            return []

    def get_cable_on_port(self, port_id):
        if not self.session_token:
            return None
        headers = {
            "Session-Token": self.session_token,
            "App-Token": self.app_token,
            "Content-Type": "application/json"
        }
        try:
            response = requests.get(f"{self.base_url}/NetworkPort/{port_id}/Cable", headers=headers)
            response.raise_for_status()
            cables = response.json()
            if cables and len(cables) > 0:
                return cables[0] # Return the first cable found
            return None
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération du câble pour le port {port_id}: {e}")
            return None

    def get_socket_details(self, socket_id):
        if not self.session_token:
            return None
        headers = {
            "Session-Token": self.session_token,
            "App-Token": self.app_token,
            "Content-Type": "application/json"
        }
        try:
            response = requests.get(f"{self.base_url}/Glpi\\Socket/{socket_id}", headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération des détails du socket {socket_id}: {e}")
            return None

    def get_cable_on_socket(self, socket_id):
        if not self.session_token:
            return None
        headers = {
            "Session-Token": self.session_token,
            "App-Token": self.app_token,
            "Content-Type": "application/json"
        }
        try:
            response = requests.get(f"{self.base_url}/Glpi\\Socket/{socket_id}/Cable", headers=headers)
            response.raise_for_status()
            cables = response.json()
            if cables and len(cables) > 0:
                return cables[0] # Return the first cable found
            return None
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération du câble pour le socket {socket_id}: {e}")
            return None

    def create_item(self, itemtype, data):
        """Crée un seul item."""
        return self.create_items(itemtype, [data], batch_size=1)

    def create_items(self, itemtype, data_list, batch_size=100):
        """Crée plusieurs items en les envoyant par lots."""
        if not self.session_token: return None
        
        all_responses = []
        # Utiliser la console de l'ApiClient s'il en a une
        console = getattr(self, 'console', Console())

        for i in range(0, len(data_list), batch_size):
            batch = data_list[i:i + batch_size]
            payload = {'input': batch}
            headers = { 'Session-Token': self.session_token, 'Content-Type': 'application/json' }
            
            try:
                response = requests.post(f"{self.base_url}/{itemtype}/", headers=headers, json=payload)
                response.raise_for_status()
                json_response = response.json()
                # Gérer le cas où la réponse est un dictionnaire avec un message d'erreur
                if isinstance(json_response, dict) and 'message' in json_response:
                     console.log(f"[bold red]Erreur de l'API GLPI pour {itemtype}: {json_response['message']}[/bold red]")
                     continue # On passe au lot suivant
                all_responses.extend(json_response)
            except requests.exceptions.RequestException as e:
                console.log(f"[bold red]Erreur réseau lors de la création d'un lot de {itemtype}: {e}[/bold red]")
                continue # On continue avec le lot suivant
        
        return all_responses




