# main.py (à la racine)
from src.shell import GLPIExplorerShell

# Ce fichier est pour le développement local.
# Le point d'entrée de l'installation est dans src/__main__.py
if __name__ == "__main__":
    shell = GLPIExplorerShell()
    shell.run()