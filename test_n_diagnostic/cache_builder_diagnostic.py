import sys
import types
from rich.console import Console
from rich import print_json

# Assurez-vous que le chemin vers src est dans sys.path
sys.path.insert(0, './src')
from api_client import ApiClient
from config_manager import ConfigManager

console = Console()

def main():
    # --- ÉTAPE 1: Initialisation et Connexion ---
    config = ConfigManager().load_config()
    if not config:
        console.print("[red]Erreur: Fichier de configuration non trouvé.[/red]")
        return
    
    api_client = ApiClient(config)
    api_client.connect()
    console.print("[green]Connexion réussie.[/green]")

    # --- ÉTAPE 2: Chargement des Données Brutes ---
    console.print("\n[cyan]--- 1. Chargement des données brutes depuis l'API ---[/cyan]")
    
    # Charger PC1 spécifiquement
    all_computers_raw = api_client.list_items('Computer', '0-9999')
    pc1_raw = next((c for c in all_computers_raw if c.get('name') == 'PC1'), None)
    if not pc1_raw:
        console.print("[red]Erreur: PC1 non trouvé.[/red]")
        return
    
    console.print("PC1 brut chargé.")
    
    # Charger tous les ports et sockets
    all_network_ports_raw = api_client.list_items('NetworkPort', '0-9999')
    console.print(f"{len(all_network_ports_raw)} NetworkPorts bruts chargés.")
    
    all_sockets_raw = api_client.list_items('Glpi\\Socket', '0-9999')
    console.print(f"{len(all_sockets_raw)} Sockets bruts chargés.")
    
    # --- ÉTAPE 3: Création des Objets Cache (simulation) ---
    console.print("\n[cyan]--- 2. Création des objets en mémoire ---[/cyan]")
    
    pc1_obj = types.SimpleNamespace(**pc1_raw)
    
    network_ports_cache = {p['id']: types.SimpleNamespace(**p) for p in all_network_ports_raw}
    sockets_cache = {s['id']: types.SimpleNamespace(**s) for s in all_sockets_raw}
    
    console.print("Objets créés.")

    # --- ÉTAPE 4: Tentative de Liaison (Logique à déboguer) ---
    console.print("\n[cyan]--- 3. Tentative de liaison hiérarchique ---[/cyan]")
    
    # On initialise l'attribut sur notre objet PC1
    pc1_obj.networkports = []
    
    # On parcourt TOUS les ports chargés
    for port in network_ports_cache.values():
        parent_id = getattr(port, 'items_id', None)
        
        console.print(f"Analyse du port '{port.name}' (ID: {port.id}). Parent ID attendu: {pc1_obj.id}. Parent ID trouvé: {parent_id}")
        
        # Si le parent d'un port est notre PC1
        if parent_id == pc1_obj.id:
            console.print(f"[bold green]  -> MATCH TROUVÉ ![/bold green] Liaison du port '{port.name}' à l'objet PC1.")
            pc1_obj.networkports.append(port)
            port.parent_item = pc1_obj

    # --- ÉTAPE 5: Affichage du Résultat Final ---
    console.print("\n[cyan]--- 4. État final de l'objet PC1 dans le cache ---[/cyan]")
    
    # On doit créer une version "sérialisable" de l'objet pour l'afficher
    final_pc1_dict = vars(pc1_obj).copy()
    if hasattr(pc1_obj, 'networkports'):
        # Remplacer la liste d'objets par une liste de noms de ports pour l'affichage
        final_pc1_dict['networkports'] = [p.name for p in pc1_obj.networkports]
        
    print_json(data=final_pc1_dict)

    # --- ÉTAPE 6: Fermeture ---
    api_client.close_session()
    console.print("\n[green]Session fermée.[/green]")

if __name__ == "__main__":
    main()