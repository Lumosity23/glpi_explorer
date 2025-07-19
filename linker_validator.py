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
        console.print("[bold red]Usage: python linker_validator.py <ID_SOCKET>[/bold red]")
        return
    
    socket_id_to_test = int(sys.argv[1])

    # --- Chargement ---
    config = ConfigManager().load_config()
    api_client = ApiClient(config)
    api_client.connect()
    cache = TopologyCache(api_client)
    cache.load_from_api(console)
    linker = TopologyLinker(cache)
    console.print("[green]Cache chargé et Linker initialisé.[/green]\n")
    
    # --- Validation ---
    console.print(Panel(f"Validation pour le Socket ID : [bold cyan]{socket_id_to_test}[/bold cyan]"))
    
    # Test 1: Trouver le socket
    socket_obj = cache.sockets.get(socket_id_to_test)
    if not socket_obj:
        console.print(f"[bold red]ÉCHEC :[/bold red] Socket {socket_id_to_test} non trouvé dans le cache.")
        return
    console.print(f"[green]SUCCÈS :[/green] Socket trouvé : '{socket_obj.name}'")

    # Test 2: Trouver le parent
    parent = linker.find_parent_for_socket(socket_obj)
    if not parent:
        console.print(f"[bold red]ÉCHEC :[/bold red] Parent pour le socket '{socket_obj.name}' non trouvé.")
        console.print(f"   (items_id du socket: {getattr(socket_obj, 'items_id', 'N/A')})")
        return
    console.print(f"[green]SUCCÈS :[/green] Parent trouvé : '{parent.name}' (Type: {parent.itemtype})")

    # Test 3: Trouver la connexion
    connection = linker.find_connection_for_socket(socket_obj)
    if not connection:
        console.print(f"[yellow]INFO :[/yellow] Pas de connexion trouvée pour ce socket (Fin de ligne).")
    else:
        other_socket = connection['other_socket']
        other_parent = linker.find_parent_for_socket(other_socket)
        console.print(f"[green]SUCCÈS :[/green] Connecté via '{connection['via_cable'].name}' à '{other_socket.name}' sur '{getattr(other_parent, 'name', 'Parent Inconnu')}'")

    api_client.close_session()

if __name__ == "__main__":
    main()
