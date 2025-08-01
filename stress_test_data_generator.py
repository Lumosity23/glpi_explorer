# stress_test_data_generator.py
import sys
import time
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, TaskProgressColumn
from rich.table import Table

sys.path.insert(0, './src')
from api_client import ApiClient
from config_manager import ConfigManager

console = Console()

def create_in_batches(api_client, itemtype, data_list, progress, task):
    """Envoie des données par lots et met à jour une barre de progression."""
    batch_size = 100 # La création en masse est plus efficace
    for i in range(0, len(data_list), batch_size):
        batch = data_list[i:i + batch_size]
        response = api_client.create_item(itemtype, batch)
        if response is None:
            console.log(f"[bold red]Échec d'un lot pour {itemtype}. Arrêt de cette étape.[/bold red]")
            break
        progress.update(task, advance=len(batch))
        time.sleep(0.1) # Petite pause pour ne pas surcharger l'API

def main():
    config = ConfigManager().load_config()
    api_client = ApiClient(config)
    if not api_client.connect():
        console.print("[red]Échec de la connexion.[/red]")
        return
    
    console.print(Panel("[bold yellow]Lancement du générateur de données de test de charge[/bold yellow]\n[dim]Ce processus peut prendre plusieurs minutes. Ne l'interrompez pas.[/dim]"))

    # --- Définition du Plan ---
    tasks = {
        "Computers": {"count": 10000, "itemtype": "Computer"},
        "Switches": {"count": 100, "itemtype": "NetworkEquipment", "ports": 48},
        "PatchPanels": {"count": 50, "itemtype": "PassiveDCEquipment", "ports": 48},
        "Walloutlets": {"count": 500, "itemtype": "PassiveDCEquipment", "ports": 4}
    }
    
    # --- Création du Tableau de Bord "Live" ---
    overall_progress = Progress(
        TextColumn("[bold blue]Progression Globale:"),
        BarColumn(),
        TaskProgressColumn(),
    )
    tasks_progress = Progress(TextColumn("  [cyan]{task.description}"), BarColumn())
    
    progress_table = Table.grid(expand=True)
    progress_table.add_row(overall_progress)
    progress_table.add_row(tasks_progress)
    
    overall_task = overall_progress.add_task("Tâches...", total=len(tasks))

    with Live(progress_table, refresh_per_second=10):
        # --- Exécution des Tâches ---
        
        # 1. Ordinateurs
        pc_task = tasks_progress.add_task("Création des Ordinateurs", total=tasks["Computers"]["count"])
        computers_to_create = [{'name': f'PERF-PC-{i:05d}'} for i in range(tasks["Computers"]["count"])]
        create_in_batches(api_client, 'Computer', computers_to_create, tasks_progress, pc_task)
        overall_progress.advance(overall_task)
        tasks_progress.stop_task(pc_task)
        tasks_progress.update(pc_task, description="[green]Création des Ordinateurs... Terminé[/green]")

        # 2. Équipements avec Ports (Switchs, PP, WO)
        for name, details in tasks.items():
            if "ports" not in details: continue # Skip Computers
            
            task = tasks_progress.add_task(f"Création des {name}", total=details["count"])
            items_to_create = [{'name': f'PERF-{name[:-1]}-{i:03d}'} for i in range(details["count"])]
            
            for item_data in items_to_create:
                # On crée les équipements un par un pour récupérer leur ID
                response = api_client.create_item(details["itemtype"], item_data)
                if response and response[0].get('id'):
                    item_id = response[0]['id']
                    
                    # Créer les NetworkPorts et Sockets associés
                    ports_to_create = []
                    sockets_to_create = []
                    
                    for p in range(details["ports"]):
                        port_name = f"Port-{p:02d}"
                        if details["itemtype"] == 'PassiveDCEquipment':
                            # Les passifs ont des paires IN/OUT
                            port_name_in = f"Port-{p:02d}-IN"
                            port_name_out = f"Port-{p:02d}-OUT"
                            sockets_to_create.append({'items_id': item_id, 'itemtype': details["itemtype"], 'name': port_name_in})
                            sockets_to_create.append({'items_id': item_id, 'itemtype': details["itemtype"], 'name': port_name_out})
                        else:
                            ports_to_create.append({'items_id': item_id, 'itemtype': details["itemtype"], 'name': port_name})
                    
                    if ports_to_create: api_client.create_items('NetworkPort', ports_to_create)
                    if sockets_to_create: api_client.create_items('Glpi\\Socket', sockets_to_create)

                tasks_progress.advance(task)
                time.sleep(0.05)
                
            overall_progress.advance(overall_task)
            tasks_progress.stop_task(task)
            tasks_progress.update(task, description=f"[green]Création des {name}... Terminé[/green]")
        
        overall_progress.stop_task(overall_task)
        overall_progress.update(overall_task, description="[bold green]Toutes les tâches sont terminées ![/bold green]")

    console.print("\n[bold green]Génération des données de test terminée avec succès ![/bold green]")
    api_client.close_session()

if __name__ == "__main__":
    # Ajout d'une nouvelle méthode create_item dans ApiClient pour gérer la taille des lots
    def create_item_with_batches(self, itemtype, data, batch_size=100):
        if not self.session_token: return None
        responses = []
        data_list = data if isinstance(data, list) else [data]
        for i in range(0, len(data_list), batch_size):
            batch = data_list[i:i + batch_size]
            payload = {'input': batch}
            headers = { 'Session-Token': self.session_token, 'Content-Type': 'application/json' }
            try:
                response = requests.post(f"{self.base_url}/{itemtype}/", headers=headers, json=payload)
                response.raise_for_status()
                responses.extend(response.json())
            except requests.exceptions.RequestException as e:
                console.log(f"[bold red]Erreur lors de la création d'un lot de {itemtype}: {e}[/bold red]")
                return None
        return responses
    
    # Remplacer la méthode existante sur l'instance d'ApiClient
    ApiClient.create_item = create_item_with_batches
    
    main()