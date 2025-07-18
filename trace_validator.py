# trace_validator.py
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print

sys.path.insert(0, './src')
from api_client import ApiClient
from config_manager import ConfigManager
from topology_cache import TopologyCache
from topology_linker import TopologyLinker

console = Console()

def main():
    if len(sys.argv) != 3:
        console.print("[bold red]Usage: python trace_validator.py <type_alias> <nom_objet>[/bold red]")
        return

    user_type_alias, item_name = sys.argv[1], sys.argv[2]

    # --- ÉTAPE 1: Chargement complet du cache ---
    config = ConfigManager().load_config()
    api_client = ApiClient(config)
    api_client.connect()
    cache = TopologyCache(api_client)
    cache.load_from_api(console)
    linker = TopologyLinker(cache)
    console.print("[green]Cache chargé et Linker initialisé.[/green]\n")

    # --- ÉTAPE 2: Démarrage de la trace ---
    itemtype = linker.cache.TYPE_ALIASES.get(user_type_alias.lower()) # Correction
    start_item = linker.find_item(itemtype, item_name)
    if not start_item:
        console.print(f"[red]Objet de départ '{item_name}' non trouvé.[/red]")
        return

    start_sockets = linker.find_sockets_for_item(start_item)
    if not start_sockets:
        console.print(f"[red]Aucun socket trouvé pour {start_item.name}.[/red]")
        return

    current_socket = start_sockets[0]
    
    # --- ÉTAPE 3: Boucle de débogage et de traçage ---
    trace_steps = []
    visited_sockets = set()
    
    console.print(Panel(f"Début de la trace pour [bold cyan]{start_item.name}[/bold cyan] en partant du socket [bold magenta]{current_socket.name}[/bold magenta]"))

    while current_socket and current_socket.id not in visited_sockets:
        visited_sockets.add(current_socket.id)
        
        parent = linker.find_parent_for_socket(current_socket)
        hop = linker.get_next_hop(current_socket)
        
        # -- LOGS DE DÉBOGAGE POUR CHAQUE ÉTAPE --
        print("\n" + "="*50)
        print(f"[bold]ÉTAPE {len(trace_steps) + 1}[/bold]")
        print(f"  - Socket Actuel : {current_socket.name} (ID: {current_socket.id})")
        print(f"  - Parent Trouvé : {getattr(parent, 'name', 'AUCUN')}")
        print(f"  - Résultat de get_next_hop() : {hop}")
        
        trace_steps.append({'socket': current_socket, 'parent': parent, 'hop': hop})
        
        if not hop or hop['type'] == 'end':
            break
        
        if hop['type'] == 'connection':
            current_socket = hop['next_socket']
        elif hop['type'] == 'traversal':
            current_socket = hop['to_socket']
    
    # --- ÉTAPE 4: Affichage final ---
    console.print("\n" + "="*50)
    console.print(Panel("[bold green]Trace Terminée. Construction du tableau de résultats...[/bold green]"))
    
    final_table = Table(title=f"Trace depuis {start_item.name}")
    # ... (logique d'affichage à perfectionner plus tard)
    final_table.add_column("Équipement")
    final_table.add_column("Port")

    for step_data in trace_steps:
        final_table.add_row(
            getattr(step_data['parent'], 'name', 'Parent Inconnu'),
            step_data['socket'].name
        )
    
    console.print(final_table)
    api_client.close_session()

if __name__ == "__main__":
    main()
