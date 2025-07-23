# main.py (à la racine)
import sys
from src.shell import GLPIExplorerShell

# Ce fichier est pour le développement local.
# Le point d'entrée de l'installation est dans src/__main__.py
if __name__ == "__main__":
    shell = GLPIExplorerShell()
    if len(sys.argv) > 2 and sys.argv[1] == '-c':
        command = ' '.join(sys.argv[2:])
        shell.run_single_command(command)
    else:
        shell.run()