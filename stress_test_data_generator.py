# stress_test_data_generator.py
import sys
import random
from rich.console import Console
from rich.progress import track

sys.path.insert(0, './src')
from api_client import ApiClient
from config_manager import ConfigManager

console = Console()

def create_in_batches(api_client, itemtype, data_list, batch_size=100):
    """Fonction d'aide pour envoyer des données par lots."""
    console.print(f"Création de {len(data_list)} objets de type [cyan]{itemtype}[/cyan]...")
    for i in track(range(0, len(data_list), batch_size), description=f"Envoi des lots pour {itemtype}..."):
        batch = data_list[i:i + batch_size]
        api_client.create_item(itemtype, batch)

def main():
    # --- Connexion ---
    config = ConfigManager().load_config()
    api_client = ApiClient(config)
    if not api_client.connect():
        console.print("[red]Échec de la connexion.[/red]")
        return

    # --- Génération des Données ---
    
    # 1. Ordinateurs (10 000)
    computers_to_create = [{'name': f'PERF-PC-{i:05d}'} for i in range(10000)]
    create_in_batches(api_client, 'Computer', computers_to_create)

    # 2. Switchs (100)
    switches_to_create = [{'name': f'PERF-SW-{i:03d}'} for i in range(100)]
    console.print("Création de 100 Switchs et de leurs ports...")
    for switch_data in track(switches_to_create, description="Création des Switchs..."):
        response = api_client.create_item('NetworkEquipment', switch_data)
        if response and response[0].get('id'):
            switch_id = response[0]['id']
            ports_to_create = [{'items_id': switch_id, 'itemtype': 'NetworkEquipment', 'name': f'port-{p}'} for p in range(50)]
            api_client.create_item('NetworkPort', ports_to_create)
    
    # 3. Patch Panels (50)
    patch_panels_to_create = [{'name': f'PERF-PP-{i:03d}'} for i in range(50)]
    console.print("Création de 50 Patch Panels et de leurs ports...")
    for pp_data in track(patch_panels_to_create, description="Création des Patch Panels..."):
        response = api_client.create_item('PassiveDCEquipment', pp_data)
        if response and response[0].get('id'):
            pp_id = response[0]['id']
            ports_to_create = [{'items_id': pp_id, 'itemtype': 'PassiveDCEquipment', 'name': f'port-{p}'} for p in range(50)]
            api_client.create_item('NetworkPort', ports_to_create)

    # 4. Walloutlets (50)
    walloutlets_to_create = [{'name': f'PERF-WO-{i:03d}'} for i in range(50)]
    console.print("Création de 50 Walloutlets et de leurs sockets...")
    for wo_data in track(walloutlets_to_create, description="Création des Walloutlets..."):
        response = api_client.create_item('PassiveDCEquipment', wo_data)
        if response and response[0].get('id'):
            wo_id = response[0]['id']
            sockets_to_create = [{'items_id': wo_id, 'itemtype': 'PassiveDCEquipment', 'name': f'socket-{s}'} for s in range(4)]
            api_client.create_item('Socket', sockets_to_create)
    
    console.print("[green]Génération des données de test terminée ![/green]")
    api_client.close_session()

if __name__ == "__main__":
    main()
