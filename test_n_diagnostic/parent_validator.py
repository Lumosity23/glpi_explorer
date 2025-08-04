import sys
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.api_client import ApiClient
from src.config_manager import ConfigManager
from src.topology_cache import TopologyCache
from src.topology_linker import TopologyLinker

def main():
    """
    Main function to run the parent validation diagnostic.
    """
    console = Console()
    console.print(Panel("[bold cyan]Démarrage de l'Outil d'Audit de la Parenté des Sockets[/bold cyan]"))

    # --- Initialisation ---
    config_manager = ConfigManager()
    config = config_manager.load_config()
    if not config:
        console.print("[bold red]Erreur:[/bold red] La configuration de l'API n'est pas définie. Veuillez exécuter le script de configuration.")
        return

    api_client = ApiClient(config)
    cache = TopologyCache(api_client)
    linker = TopologyLinker(cache)

    try:
        with console.status("[bold green]Connexion à l'API GLPI...[/bold green]"):
            api_client.connect()
        
        with console.status("[bold green]Chargement du cache de topologie depuis l'API...[/bold green]"):
            cache.load_from_api(console=console)

        console.print("[green]✓ Cache chargé et liens de topologie créés.[/green]")

        # --- Logique d'Audit ---
        table = Table(title="[bold]Rapport d'Audit de Parenté des Sockets[/bold]")
        table.add_column("ID Socket", justify="right", style="cyan", no_wrap=True)
        table.add_column("Nom Socket", style="magenta")
        table.add_column("Parent Attendu (du nom)", style="yellow")
        table.add_column("Parent Réel (de GLPI)", style="blue")
        table.add_column("Statut", justify="center")

        inconsistencies_count = 0
        
        # Create a list of all potential parent items to search through
        all_items = list(cache.computers.values()) + list(cache.network_equipments.values()) + list(cache.passive_devices.values())

        for socket in cache.sockets.values():
            socket_id = str(getattr(socket, 'id', 'N/A'))
            socket_name = getattr(socket, 'name', 'N/A')

            # b. Find the real parent using the linker
            real_parent = linker.find_parent_for_socket(socket)
            real_parent_name = getattr(real_parent, 'name', 'INCONNU') if real_parent else 'AUCUN'

            # d. Heuristic to find the expected parent from the socket name
            expected_parent_name = 'INDÉTERMINÉ'
            for item in all_items:
                item_name = getattr(item, 'name', '')
                if item_name and item_name.lower() in socket_name.lower():
                    expected_parent_name = item_name
                    break # Take the first match

            # e. Compare and determine status
            status = "[green]OK[/green]"
            if expected_parent_name != 'INDÉTERMINÉ' and expected_parent_name != real_parent_name:
                status = "[bold red]INCOHÉRENCE[/bold red]"
                inconsistencies_count += 1
            
            # h. Add row to the table
            table.add_row(socket_id, socket_name, expected_parent_name, real_parent_name, status)

        # --- Affichage ---
        console.print(table)

        summary_color = "green" if inconsistencies_count == 0 else "yellow"
        summary_message = f"Audit terminé. Nombre d'incohérences trouvées : {inconsistencies_count}"
        console.print(Panel(summary_message, title="[bold]Conclusion de l'Audit[/bold]", style=summary_color))

    except Exception as e:
        console.print(f"[bold red]Une erreur critique est survenue :[/bold red] {e}")
    finally:
        # --- Fermeture ---
        api_client.close_session()
        console.print("[cyan]Session API fermée.[/cyan]")

if __name__ == "__main__":
    main()
