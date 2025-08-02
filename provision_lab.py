# provision_lab.py
import sys
from rich.console import Console
from rich import print

sys.path.insert(0, './src')
from api_client import ApiClient
from config_manager import ConfigManager

console = Console()

class Provisioner:
    def __init__(self, api_client):
        self.api = api_client

    def _create_item(self, itemtype, data, label):
        console.print(f"- Création de {label} '{data['name']}'...")
        # La méthode create_item retourne maintenant une liste, même pour un seul item
        response = self.api.create_item(itemtype, data)
        if not (response and isinstance(response, list) and response[0].get('id')):
            console.print(f"[bold red]  -> ÉCHEC.[/bold red] Réponse: {response}")
            raise RuntimeError(f"Échec de la création de {label}")
        
        item_id = response[0]['id']
        console.print(f"  -> [green]SUCCÈS.[/green] ID: {item_id}")
        return item_id

    def create_socket(self, parent_id, parent_type, socket_name):
        # L'API GLPI peut nécessiter l'itemtype complet pour la liaison
        glpi_parent_type = "Computer" if parent_type == "Computer" else "PassiveDCEquipment" if parent_type == "PassiveDCEquipment" else "NetworkEquipment"

        socket_data = {'items_id': parent_id, 'itemtype': glpi_parent_type, 'name': socket_name}
        return self._create_item('Glpi\\Socket', socket_data, "Socket")

    def create_cable(self, name, socket_a_id, socket_b_id):
        # La connexion se fait maintenant avec une mise à jour PUT
        # Étape 1: Créer le câble
        cable_id = self._create_item('Cable', {'name': name}, "Câble")
        
        # Étape 2: Mettre à jour le câble pour connecter les sockets
        console.print(f"- Connexion du câble '{name}'...")
        update_payload = {
            'sockets_id_endpoint_a': socket_a_id,
            'sockets_id_endpoint_b': socket_b_id
        }
        update_response = self.api.update_item('Cable', cable_id, update_payload)
        
        if update_response and update_response[0].get(str(cable_id)) is True:
             console.print(f"  -> [green]SUCCÈS.[/green] Câble connecté.")
        else:
            console.print(f"[bold red]  -> ÉCHEC.[/bold red] Réponse: {update_response}")
            raise RuntimeError(f"Échec de la connexion du câble {name}")
        return cable_id

    def run(self):
        try:
            console.print("[bold blue]=== DÉBUT DU PROVISIONING AVEC LE NOUVEL API CLIENT ===[/bold blue]")

            # 1. Équipements
            pc_id = self._create_item('Computer', {'name': 'PROV-PC-01'}, "PC")
            wo_id = self._create_item('PassiveDCEquipment', {'name': 'PROV-WO-01'}, "Walloutlet")
            pp_id = self._create_item('PassiveDCEquipment', {'name': 'PROV-PP-01'}, "Patch Panel")
            sw_id = self._create_item('NetworkEquipment', {'name': 'PROV-SW-01'}, "Switch")

            # 2. Sockets
            pc_socket_id = self.create_socket(pc_id, 'Computer', 'PC-Port-1')
            wo_in_id = self.create_socket(wo_id, 'PassiveDCEquipment', 'WO-Port-1-IN')
            wo_out_id = self.create_socket(wo_id, 'PassiveDCEquipment', 'WO-Port-1-OUT')
            pp_in_id = self.create_socket(pp_id, 'PassiveDCEquipment', 'PP-Port-1-IN')
            pp_out_id = self.create_socket(pp_id, 'PassiveDCEquipment', 'PP-Port-1-OUT')
            sw_socket_id = self.create_socket(sw_id, 'NetworkEquipment', 'SW-Port-1')

            # 3. Câbles
            self.create_cable('C-PC-WO', pc_socket_id, wo_in_id)
            self.create_cable('C-WO-PP', wo_out_id, pp_in_id)
            self.create_cable('C-PP-SW', pp_out_id, sw_socket_id)

            console.print("\n[bold green]=== PROVISIONING TERMINÉ AVEC SUCCÈS ===[/bold green]")

        except RuntimeError as e:
            console.print(f"\n[bold red]=== LE PROVISIONING A ÉCHOUÉ ===[/bold red]")
            console.print(f"Raison: {e}")
        except Exception as e:
            console.print(f"\n[bold red]Une erreur inattendue est survenue: {e}[/bold red]")

def main():
    config = ConfigManager().load_config()
    api_client = ApiClient(config)
    if not api_client.connect(): return

    provisioner = Provisioner(api_client)
    provisioner.run()

    api_client.close_session()

if __name__ == "__main__":
    main()