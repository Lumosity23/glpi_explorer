# src/__main__.py
from .shell import GLPIExplorerShell

def main():
    """Point d'entrée principal pour l'application."""
    shell = GLPIExplorerShell()
    shell.run()

if __name__ == "__main__":
    main()