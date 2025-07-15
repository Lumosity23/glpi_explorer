import sys
import os

# Ajouter le répertoire src au PYTHONPATH pour les imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from api_client import ApiClient
from config_manager import ConfigManager


if __name__ == "__main__":
    console = Console()
    console.rule("[bold cyan]Lancement du Script de Test API GLPI[/bold cyan]")

    config_manager = ConfigManager()
    try:
        config = config_manager.load_config()
        if not config:
            console.print("[bold red]ERREUR:[/bold red] Configuration GLPI invalide ou manquante. Assurez-vous que ~/.config/glpi-explorer/config.json existe et est valide.")
            sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]ERREUR:[/bold red] Impossible de charger la configuration: {e}")
        sys.exit(1)

    api_client = ApiClient(config)

    try:
        console.print("\n[bold blue]Tentative de connexion à l'API GLPI...[/bold blue]")
        api_client.connect()
        console.print("[green]SUCCÈS:[/green] Connexion à l'API GLPI établie.")

        # Test 1: Listing des Itemtypes
        console.rule("Test 1: Listing des 5 premiers objets par itemtype")
        itemtypes_to_test = ['Computer', 'NetworkEquipment', 'PassiveDevice', 'PassiveEquipment', 'PDU', 'Rack', 'Enclosure', 'Cable']

        for itemtype in itemtypes_to_test:
            try:
                items = api_client.list_items(itemtype)
                if items:
                    console.print(f"[green]SUCCÈS[/green] - {len(items)} objets trouvés pour l'itemtype '[bold]{itemtype}[/bold]'")
                    # Afficher les 5 premiers pour un aperçu
                    for i, item in enumerate(items[:5]):
                        console.print(f"  - [dim]{item.get('name', 'Nom inconnu')} (ID: {item.get('id', 'N/A')})[/dim]")
                else:
                    console.print(f"[yellow]ÉCHEC/VIDE[/yellow] - Aucun objet trouvé ou itemtype invalide pour '[bold]{itemtype}[/bold]'")
            except Exception as e:
                console.print(f"[bold red]ERREUR[/bold red] lors du listing de '[bold]{itemtype}[/bold]': {e}")

        # Test 2: Recherche d'un objet spécifique
        console.rule("Test 2: Recherche de 'PC1' via search_item")
        try:
            item_id = api_client.search_item('Computer', 'PC1')
            if item_id is not None:
                console.print(f"[green]SUCCÈS[/green] - 'PC1' trouvé avec l'ID: [bold]{item_id}[/bold]")
            else:
                console.print("[bold red]ÉCHEC[/bold red] - La recherche de 'PC1' a échoué.")
        except Exception as e:
            console.print(f"[bold red]ERREUR[/bold red] lors de la recherche de 'PC1': {e}")

    except Exception as e:
        console.print(f"[bold red]ERREUR FATALE:[/bold red] {e}")
        sys.exit(1)
    finally:
        console.print("\n[bold blue]Fermeture de la session API...[/bold blue]")
        api_client.close_session()
        console.print("[green]SUCCÈS:[/green] Session API fermée.")

    console.rule("[bold cyan]Fin du Script de Test API GLPI[/bold cyan]")


