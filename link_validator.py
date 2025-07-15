import sys
import types
from rich.console import Console
from rich.panel import Panel
from rich import print

# Assurez-vous que le chemin vers src est dans sys.path
sys.path.insert(0, './src')
from api_client import ApiClient
from config_manager import ConfigManager
from topology_cache import TopologyCache

console = Console()

def main():
    if len(sys.argv) != 2:
        console.print("[bold red]Usage: python link_validator.py <ID_DU_SOCKET_DE_DEPART>[/bold red]")
        return

    start_socket_id = int(sys.argv[1])

    # --- ÉTAPE 1: Chargement complet du cache ---
    config = ConfigManager().load_config()
    if not config:
        console.print("[red]Erreur: Fichier de configuration non trouvé.[/red]")
        return
    
    api_client = ApiClient(config)
    api_client.connect()
    
    console.print("[cyan]Chargement complet du cache de topologie...[/cyan]")
    cache = TopologyCache(api_client)
    cache.load_from_api(console) # Affiche la barre de progression
    console.print("[green]Cache chargé.[/green]\n")

    # --- ÉTAPE 2: Validation ---
    console.print(Panel(f"Validation de la liaison depuis le Socket ID: [bold yellow]{start_socket_id}[/bold yellow]"))

    # 2a. Trouver le socket de départ dans le cache
    start_socket = cache.sockets.get(start_socket_id)
    if not start_socket:
        console.print(f"[bold red]ERREUR :[/bold red] Le socket de départ avec l'ID {start_socket_id} n'a pas été trouvé dans le cache.")
        return
    
    console.print(f"[green]ÉTAPE 1 :[/green] Socket de départ trouvé : [cyan]{start_socket.name}[/cyan]")

    # 2b. Trouver le câble connecté
    found_cable = None
    for cable in cache.cables.values():
        socket_ids = []
        for link in getattr(cable, 'links', []):
            if link.get('rel') == 'Glpi\Socket':
                try:
                    socket_id_from_link = int(link['href'].split('/')[-1])
                    socket_ids.append(socket_id_from_link)
                except (ValueError, IndexError):
                    continue
        
        if start_socket_id in socket_ids:
            found_cable = cable
            break

    if not found_cable:
        console.print(f"[bold red]ERREUR :[/bold red] Aucun câble trouvé connecté au socket {start_socket_id}.")
        return
    
    console.print(f"[green]ÉTAPE 2 :[/green] Câble trouvé : [cyan]{found_cable.name}[/cyan] (ID: {found_cable.id})")

    # 2c. Trouver l'autre socket à l'extrémité du câble
    other_socket_id = None
    # On re-parcourt les liens du câble trouvé
    socket_ids_in_cable = []
    for link in getattr(found_cable, 'links', []):
        if link.get('rel') == 'Glpi\Socket':
            try:
                socket_ids_in_cable.append(int(link['href'].split('/')[-1]))
            except (ValueError, IndexError):
                continue

    if len(socket_ids_in_cable) == 2:
        id1, id2 = socket_ids_in_cable
        other_socket_id = id2 if id1 == start_socket_id else id1
    
    if not other_socket_id:
        console.print(f"[bold red]ERREUR :[/bold red] Impossible de déterminer l'autre extrémité du câble {found_cable.name}.")
        return
        
    console.print(f"[green]ÉTAPE 3 :[/green] ID de l'autre socket trouvé : [cyan]{other_socket_id}[/cyan]")
    
    # 2d. Trouver l'objet de l'autre socket dans le cache
    other_socket = cache.sockets.get(other_socket_id)
    if not other_socket:
        console.print(f"[bold red]ERREUR :[/bold red] L'objet pour le socket ID {other_socket_id} n'existe pas dans le cache.")
        return

    console.print(f"[green]ÉTAPE 4 :[/green] Autre socket trouvé : [cyan]{other_socket.name}[/cyan]")
    
    console.print("\n[bold green]VALIDATION RÉUSSIE : La liaison Socket-Câble-Socket est fonctionnelle ![/bold green]")

    # --- ÉTAPE 3: Fermeture ---
    api_client.close_session()

if __name__ == "__main__":
    main()