import sys
import json
from rich.console import Console
from rich.panel import Panel
from rich import print_json

sys.path.insert(0, './src')

from api_client import ApiClient
from config_manager import ConfigManager

console = Console()

def main():
    config_manager = ConfigManager()
    config = config_manager.load_config()

    if not config:
        console.print(Panel(
            "[bold red]Erreur:[/bold red] Configuration GLPI introuvable.",
            title="[red]Erreur de Configuration[/red]"
        ))
        sys.exit(1)

    api_client = ApiClient(config)
    is_connected = False
    try:
        console.print("[bold blue]--- CONNEXION À L'API GLPI ---[/bold blue]")
        if not api_client.connect():
            console.print("[bold red]Échec de la connexion.[/bold red]")
            sys.exit(1)
        
        is_connected = True
        console.print("[bold green]Connexion réussie.[/bold green]")

        console.print("[bold blue]--- LISTE DES CÂBLES ---[/bold blue]")
        cables = api_client.list_items('Cable', item_range="0-9999")

        if not cables:
            console.print(Panel(f"Aucun câble trouvé dans GLPI.", title="[yellow]Information[/yellow]"))
            sys.exit(0)

        console.print(f"[bold blue]Câbles trouvés ({len(cables)}):[/bold blue]")
        print_json(data=cables[:5]) # Print first 5 cables

        # Get details of the first cable
        first_cable_id = cables[0].get("id")
        first_cable_name = cables[0].get("name")
        console.print(f"[bold blue]--- RÉCUPÉRATION DES DÉTAILS DU CÂBLE '{first_cable_name}' (ID: {first_cable_id}) ---[/bold blue]")
        cable_details = api_client.get_item_details('Cable', first_cable_id)
        console.print("[bold blue]Détails complets du câble (JSON brut):[/bold blue]")
        print_json(data=cable_details)

    except Exception as e:
        console.print(Panel(
            f"[bold red]Une erreur est survenue:[/bold red] {e}",
            title="[red]Erreur[/red]"
        ))
    finally:
        if is_connected:
            api_client.close_session()
            console.print("[bold green]Session API fermée.[/bold green]")

if __name__ == "__main__":
    main()