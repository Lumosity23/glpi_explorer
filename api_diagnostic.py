import sys
import json
from rich.console import Console
from rich.panel import Panel
from rich import print_json

# Assurez-vous que le chemin vers src est dans sys.path
sys.path.insert(0, './src')

from src.api_client import ApiClient
from src.config_manager import ConfigManager

console = Console()

TYPE_ALIASES = {
    'computer': 'Computer', 'pc': 'Computer',
    'monitor': 'Monitor', 'screen': 'Monitor',
    'networkequipment': 'NetworkEquipment', 'network': 'NetworkEquipment',
    'switch': 'NetworkEquipment', 'sw': 'NetworkEquipment',
    'hub': 'NetworkEquipment', 'hb': 'NetworkEquipment',
    'peripheral': 'Peripheral',
    'phone': 'Phone',
    'printer': 'Printer',
    'software': 'Software',
    'ticket': 'Ticket',
    'user': 'User',
    'patchpanel': 'PassiveDCEquipment', 'patch': 'PassiveDCEquipment',
    'pp': 'PassiveDCEquipment',
    'walloutlet': 'PassiveDCEquipment', 'wo': 'PassiveDCEquipment',
    'cable': 'Cable', 'cb': 'Cable',
    'socket': 'Glpi\\Socket', 
    'socketmodel': 'Glpi\\SocketModel',
}

def _get_item_type(user_type_alias: str) -> str:
    return TYPE_ALIASES.get(user_type_alias.lower(), user_type_alias)

def main():
    if len(sys.argv) != 3:
        console.print(Panel(
            "[bold red]Erreur:[/bold red] Utilisation: python api_diagnostic.py <mode> <id>\nModes: cable_on_port, socket_details, socketmodel_details",
            title="[red]Utilisation[/red]"
        ))
        sys.exit(1)

    mode = sys.argv[1]
    item_id = sys.argv[2]

    config_manager = ConfigManager()
    config = config_manager.load_config()

    if not config:
        console.print(Panel(
            "[bold red]Erreur:[/bold red] Configuration GLPI introuvable. Veuillez exécuter l'application principale pour la configurer.",
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

        if mode == "cable_on_port":
            console.print(f"[bold blue]--- RÉCUPÉRATION DU CÂBLE POUR LE PORT (ID: {item_id}) ---[/bold blue]")
            cable_info = api_client.get_cable_on_port(item_id)
            if cable_info:
                console.print("[bold blue]Réponse complète des détails du câble (JSON brut):[/bold blue]")
                print_json(data=cable_info)
            else:
                console.print(Panel(f"[bold red]Aucun câble trouvé pour le port ID: {item_id}.[/bold red]", title="[red]Information[/red]"))
        elif mode == "socket_details":
            console.print(f"[bold blue]--- RÉCUPÉRATION DES DÉTAILS DU SOCKET (ID: {item_id}) ---[/bold blue]")
            socket_details = api_client.get_socket_details(item_id)
            if socket_details:
                console.print("[bold blue]Réponse complète des détails du socket (JSON brut):[/bold blue]")
                print_json(data=socket_details)
            else:
                console.print(Panel(f"[bold red]Impossible de récupérer les détails pour le socket ID: {item_id}.[/bold red]", title="[red]Erreur[/red]"))
        elif mode == "socketmodel_details":
            console.print(f"[bold blue]--- RÉCUPÉRATION DES DÉTAILS DU SOCKET MODEL (ID: {item_id}) ---[/bold blue]")
            socketmodel_details = api_client.get_item_details("Glpi\\SocketModel", item_id)
            if socketmodel_details:
                console.print("[bold blue]Réponse complète des détails du socket model (JSON brut):[/bold blue]")
                print_json(data=socketmodel_details)
            else:
                console.print(Panel(f"[bold red]Impossible de récupérer les détails pour le socket model ID: {item_id}.[/bold red]", title="[red]Erreur[/red]"))
        else:
            console.print(Panel("[bold red]Mode de diagnostic inconnu.[/bold red]", title="[red]Erreur[/red]"))

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
