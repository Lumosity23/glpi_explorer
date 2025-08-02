import requests
import json
from rich.console import Console

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
    """Crée UN SEUL item dans GLPI."""
    if not self.session_token: return None
    
    console = getattr(self, 'console', Console())
    
    # --- DÉBUT DE LA CORRECTION ---
    # Pour un seul item, la valeur de 'input' est un OBJET
    payload = {'input': data}
    # --- FIN DE LA CORRECTION ---
    
    headers = { 'Session-Token': self.session_token, 'Content-Type': 'application/json' }
    
    try:
        url = f"{self.base_url.rstrip('/')}/{itemtype}/"
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        console.log(f"[bold red]Erreur lors de la création de {itemtype} ({data.get('name')}): {e}[/bold red]")
        return None

def create_items(self, itemtype, data_list):
    """Crée PLUSIEURS items dans GLPI en un seul appel."""
    if not self.session_token or not data_list: return None
    
    console = getattr(self, 'console', Console())
    
    # --- DÉBUT DE LA CORRECTION ---
    # Pour plusieurs items, la valeur de 'input' est une LISTE D'OBJETS
    payload = {'input': data_list}
    # --- FIN DE LA CORRECTION ---
    
    headers = { 'Session-Token': self.session_token, 'Content-Type': 'application/json' }
    
    try:
        url = f"{self.base_url.rstrip('/')}/{itemtype}/"
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        console.log(f"[bold red]Erreur lors de la création du lot de {itemtype}: {e}[/bold red]")
        return None

    def update_item(self, itemtype, item_id, data):
        """Met à jour un item existant dans GLPI."""
        if not self.session_token: return None
        
        payload = {'input': data}
        headers = { 'Session-Token': self.session_token, 'Content-Type': 'application/json' }
        
        try:
            url = f"{self.base_url.rstrip('/')}/{itemtype}/{item_id}"
            response = requests.put(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            console = getattr(self, 'console', Console())
            console.print(f"[bold red]Erreur lors de la mise à jour de {itemtype} (ID:{item_id}): {e}[/bold red]")
            if response:
                console.print(f"[bold red]Réponse de l'API : {response.text}[/bold red]")
            return None




