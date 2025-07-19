# linker_validator.py
import sys
from rich.console import Console
from rich.panel import Panel

sys.path.insert(0, './src')
from api_client import ApiClient
from config_manager import ConfigManager
from topology_cache import TopologyCache
from topology_linker import TopologyLinker

console = Console()

def main():
    if len(sys.argv) != 2:
        console.print("[bold red]Usage: python linker_validator.py <ID_SOCKET_DE_DEPART>[/bold red]")
        return
    
    start_socket_id = int(sys.argv[1])

    # --- Chargement ---
    config = ConfigManager().load_config()
    api_client = ApiClient(config)
    api_client.connect()
    cache = TopologyCache(api_client)
    cache.load_from_api(console)
    linker = TopologyLinker(cache)
    console.print("[green]Cache chargé et Linker initialisé.[/green]\n")
    
    # --- Validation ---
    console.print(Panel(f"Validation de la logique 'get_next_hop' depuis le Socket ID: [bold cyan]{start_socket_id}[/bold cyan]"))
    
    start_socket = cache.sockets.get(start_socket_id)
    if not start_socket:
        console.print(f"[bold red]ERREUR :[/bold red] Socket {start_socket_id} non trouvé.")
        return
    console.print(f"Socket de départ : '{start_socket.name}' sur '{getattr(linker.find_parent_for_socket(start_socket), 'name', 'Parent Inconnu')}'")

    hop = linker.get_next_hop(start_socket)

    console.print("\n[bold yellow]--- Résultat de get_next_hop() ---")
    if not hop:
        console.print("  Résultat : None")
    else:
        console.print(f"  Type de saut : [bold green]{hop.get('type')}[/bold green]")
        if hop['type'] == 'connection':
            console.print(f"  Via Câble    : {hop['via_cable'].name}")
            console.print(f"  Vers Socket  : {hop['next_socket'].name}")
        elif hop['type'] == 'traversal']:
            console.print(f"  Via Équipement : {hop['via_device'].name}")
            console.print(f"  De Socket      : {hop['from_socket'].name}")
            console.print(f"  À Socket       : {hop['to_socket'].name}")
        elif hop['type'] == 'traversal_entry':
            console.print(f"  Via Câble      : {hop['via_cable'].name}")
            console.print(f"  Arrivée sur    : {hop['entry_socket'].name} (sur {hop['via_device'].name})")
            console.print(f"  Sortie par     : {hop['exit_socket'].name}")
        elif hop['type'] == 'end':
            console.print(f"  Raison       : {hop.get('reason')}")

    api_client.close_session()

if __name__ == "__main__":
    main()