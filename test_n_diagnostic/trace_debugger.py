import sys
import os
from rich.console import Console
from rich.panel import Panel

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.api_client import ApiClient
from src.config_manager import ConfigManager
from src.topology_cache import TopologyCache
from src.topology_linker import TopologyLinker
from src.commands.base_command import BaseCommand

def main():
    """
    Main function to run the trace debugger.
    """
    console = Console()

    # --- Argument Parsing ---
    if len(sys.argv) != 3:
        console.print("[bold red]Usage:[/bold red] python test_n_diagnostic/trace_debugger.py <type_alias> <nom_objet>")
        return

    type_alias = sys.argv[1]
    item_name = sys.argv[2]

    console.print(Panel(f"[bold cyan]Démarrage du Débogueur de Trace pour:[/bold cyan] {type_alias} '{item_name}'"))

    # --- Initialisation ---
    config_manager = ConfigManager()
    config = config_manager.load_config()
    if not config:
        console.print("[bold red]Erreur:[/bold red] La configuration de l'API n'est pas définie.")
        return

    api_client = ApiClient(config)
    cache = TopologyCache(api_client)
    linker = TopologyLinker(cache)

    try:
        with console.status("[bold green]Connexion à l'API GLPI...[/bold green]"):
            api_client.connect()
        
        with console.status("[bold green]Chargement du cache de topologie...[/bold green]"):
            cache.load_from_api(console=console)

        console.print("[green]✓ Cache chargé et topologie prête.[/green]")

        # --- Démarrage de la Trace ---
        glpi_itemtype = BaseCommand.TYPE_ALIASES.get(type_alias.lower())
        if not glpi_itemtype:
            console.print(f"[bold red]Erreur:[/bold red] Alias de type '{type_alias}' inconnu.")
            return

        start_item = linker.find_item(glpi_itemtype, item_name)
        if not start_item:
            console.print(f"[bold red]Erreur:[/bold red] Impossible de trouver l'objet '{item_name}' de type '{glpi_itemtype}'.")
            return

        start_sockets = linker.find_sockets_for_item(start_item)
        if not start_sockets:
            console.print(f"[bold red]Erreur:[/bold red] Aucun socket trouvé pour '{item_name}'.")
            return
        
        current_socket = start_sockets[0]
        console.print(f"[yellow]Point de départ :[/yellow] Socket '{current_socket.name}' (ID: {current_socket.id}) sur {item_name}")

        # --- Boucle de Débogage ---
        trace_steps = []
        visited_sockets = set()
        step_counter = 1

        while current_socket and getattr(current_socket, 'id', None) not in visited_sockets:
            socket_id = getattr(current_socket, 'id', None)
            if socket_id is None: break
            
            visited_sockets.add(socket_id)

            parent = linker.find_parent_for_socket(current_socket)
            hop = linker.get_next_hop(current_socket)

            # --- AFFICHAGE DES LOGS DE DÉBOGAGE ---
            console.print(f"\n[bold blue]====== ÉTAPE {step_counter} ======[/bold blue]")
            console.print(f"[bold]Socket Actuel :[/bold] {getattr(current_socket, 'name', 'N/A')} (ID: {socket_id})")
            console.print(f"[bold]Détails Socket :[/bold] {current_socket}")
            console.print(f"[bold]Parent Trouvé :[/bold] {getattr(parent, 'name', 'AUCUN')}")
            console.print(f"[bold]Résultat Hop :[/bold] {hop}")

            trace_steps.append({'socket': current_socket, 'parent': parent, 'hop': hop})

            if hop.get('type') == 'end':
                console.print("\n[yellow]Fin de la trace détectée.[/yellow]")
                break
            
            # Mise à jour pour le prochain saut
            if 'next_socket' in hop:
                current_socket = hop['next_socket']
            elif 'to' in hop: # Pour les traversées
                current_socket = hop['to']
            else:
                current_socket = None
            
            step_counter += 1

        console.print(Panel("[bold green]Trace de débogage terminée.[/bold green]"))

    except Exception as e:
        console.print(f"[bold red]Une erreur critique est survenue :[/bold red] {e}")
        import traceback
        traceback.print_exc()
    finally:
        # --- Fermeture ---
        api_client.close_session()
        console.print("[cyan]Session API fermée.[/cyan]")

if __name__ == "__main__":
    main()
