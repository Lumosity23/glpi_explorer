# poc_creation.py
import sys
from rich.console import Console
from rich import print

sys.path.insert(0, './src')
from api_client import ApiClient
from config_manager import ConfigManager

console = Console()

def main():
    # --- Connexion ---
    config = ConfigManager().load_config()
    api_client = ApiClient(config)
    if not api_client.connect():
        console.print("[red]Échec de la connexion.[/red]"); return
    
    console.print("[green]Connecté à l'API GLPI.[/green]")

    pc_response = None
    switch_response = None
    try:
        # --- 1. Création des Équipements ---
        console.print("\n[cyan]1. Création d'un PC et d'un Switch...[/cyan]")
        pc_data = {'name': 'POC-PC-01'}
        pc_response = api_client.create_item('Computer', pc_data)
        pc_id = pc_response['id']
        console.print(f"  - PC 'POC-PC-01' créé avec l'ID : [bold]{pc_id}[/bold]")

        switch_data = {'name': 'POC-SW-01'}
        switch_response = api_client.create_item('NetworkEquipment', switch_data)
        switch_id = switch_response['id']
        console.print(f"  - Switch 'POC-SW-01' créé avec l'ID : [bold]{switch_id}[/bold]")

        # --- 2. Création des NetworkPorts ---
        console.print("\n[cyan]2. Création des NetworkPorts...[/cyan]")
        pc_port_data = {'items_id': pc_id, 'itemtype': 'Computer', 'name': 'eth0'}
        pc_port_response = api_client.create_item('NetworkPort', pc_port_data)
        pc_port_id = pc_port_response['id']
        console.print(f"  - Port 'eth0' pour PC (ID:{pc_id}) créé avec l'ID : [bold]{pc_port_id}[/bold]")

        sw_port_data = {'items_id': switch_id, 'itemtype': 'NetworkEquipment', 'name': 'port-01'}
        sw_port_response = api_client.create_item('NetworkPort', sw_port_data)
        sw_port_id = sw_port_response['id']
        console.print(f"  - Port 'port-01' pour Switch (ID:{switch_id}) créé avec l'ID : [bold]{sw_port_id}[/bold]")

        # --- 3. Création des Sockets ---
        console.print("\n[cyan]3. Création des Sockets Physiques...[/cyan]")
        pc_socket_data = {'items_id': pc_id, 'itemtype': 'Computer', 'networkports_id': pc_port_id, 'name': 'PC-Socket-eth0'}
        pc_socket_response = api_client.create_item('Glpi\\Socket', pc_socket_data)
        pc_socket_id = pc_socket_response['id']
        console.print(f"  - Socket pour PC (Port ID:{pc_port_id}) créé avec l'ID : [bold]{pc_socket_id}[/bold]")

        sw_socket_data = {'items_id': switch_id, 'itemtype': 'NetworkEquipment', 'networkports_id': sw_port_id, 'name': 'SW-Socket-01'}
        sw_socket_response = api_client.create_item('Glpi\\Socket', sw_socket_data)
        sw_socket_id = sw_socket_response['id']
        console.print(f"  - Socket pour Switch (Port ID:{sw_port_id}) créé avec l'ID : [bold]{sw_socket_id}[/bold]")

        # --- 4. Création et Connexion du Câble ---
        console.print("\n[cyan]4. Création et connexion du Câble...[/cyan]")
        cable_data = {'name': 'POC-CABLE-01'}
        cable_response = api_client.create_item('Cable', cable_data)
        cable_id = cable_response['id']
        console.print(f"  - Câble 'POC-CABLE-01' créé avec l'ID : [bold]{cable_id}[/bold]")

        # Mettre à jour le câble pour le connecter
        update_payload = {
            'sockets_id_endpoint_a': pc_socket_id,
            'sockets_id_endpoint_b': sw_socket_id
        }
        update_response = api_client.update_item('Cable', cable_id, update_payload)
        if update_response:
            console.print(f"  - [bold green]SUCCÈS :[/bold green] Câble (ID:{cable_id}) connecté entre Socket {pc_socket_id} et Socket {sw_socket_id}.")

    except (TypeError, IndexError, KeyError) as e:
        console.print(f"[bold red]Une erreur est survenue : {e}. Vérifiez les réponses de l'API.[/bold red]")
        if pc_response: console.print("Réponse PC:", pc_response)
        if switch_response: console.print("Réponse Switch:", switch_response)
        # Ajoutez d'autres prints de debug si nécessaire

    finally:
        api_client.close_session()
        console.print("\n[green]Session fermée.[/green]")

if __name__ == "__main__":
    main()
