from src.shell import GLPIExplorerShell
from src.config_manager import ConfigManager
from src.api_client import ApiClient
from src.topology_cache import TopologyCache
from rich.console import Console

def run_debug_commands():
    console = Console()
    shell = GLPIExplorerShell(console)

    config_manager = ConfigManager()
    config = config_manager.load_config()
    if not shell._is_config_valid(config):
        console.print("Config is invalid. Aborting.")
        return

    shell.api_client = ApiClient(config)
    if not shell.api_client.connect():
        console.print("API connection failed. Aborting.")
        return

    shell.cache = TopologyCache(shell.api_client)
    shell.cache.load_from_api(console)
    shell._load_commands()

    console.print("\n--- Running 'debug cache' ---\n")
    if 'debug' in shell.commands:
        shell.commands['debug'].execute('cache')
    else:
        console.print("Debug command not found.")

    console.print("\n--- Running 'list pc' ---\n")
    if 'list' in shell.commands:
        shell.commands['list'].execute('pc')
    else:
        console.print("List command not found.")

    console.print("\n--- Running 'get pc pc1' ---\n")
    if 'get' in shell.commands:
        shell.commands['get'].execute('pc pc1')
    else:
        console.print("Get command not found.")
    
    if shell.api_client:
        shell.api_client.close_session()

if __name__ == "__main__":
    run_debug_commands()
