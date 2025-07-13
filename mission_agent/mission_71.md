Parfait. Feu vert reçu pour la Mission 7.1. C'est une mission de "nettoyage" essentielle avant de construire le cache.

---

### **PROMPT DE MISSION POUR GEMINI CLI**

**À:** Gemini CLI, notre Exécutant IA
**De:** L'Équipe d'Architecture (Projet GLPI Explorer)

---

#### **`## [MISSION 7.1] - Consolidation et Nettoyage de la Structure du Projet`**

**Rôle et Mission :**
Votre rôle est celui d'un **Ingénieur Qualité Logicielle**. Votre mission est de nettoyer et d'harmoniser le code existant pour corriger les incohérences d'importation dans les fichiers de test et simplifier la logique de chargement des commandes dans le shell principal.

**Contexte :**
Le projet est basé sur le dernier livrable. Une phase d'expérimentation rapide a laissé des incohérences :
1.  Les fichiers de test (`test_*.py`) utilisent des chemins d'importation invalides, ce qui les rend inutilisables.
2.  La manière dont la commande `help` est instanciée dans `shell.py` est un cas particulier qui complexifie le code.

**Objectif Principal :**
1.  Rendre tous les scripts de test et de diagnostic exécutables en corrigeant leurs `import`.
2.  Standardiser l'instanciation de toutes les commandes, y compris `help`, pour que la logique de chargement soit uniforme et simple.

---

#### **Base de Connaissances et Directives Permanentes :**

*   **Imports de Scripts :** Un script exécuté à la racine du projet (comme `test_api.py`) doit importer un module de `src` en utilisant `from src.module import ...`. Le `PYTHONPATH` doit être correctement configuré ou manipulé pour que cela fonctionne. La méthode la plus robuste est d'ajouter `sys.path.insert(0, './src')` en haut des scripts de test, mais nous avons déjà déplacé cette logique dans le `main.py` pour l'application principale. Assurons-nous que tous les fichiers suivent la même logique.
*   **Conception Logique :** La classe `HelpCommand` a besoin de connaître la liste des autres commandes. Cette information doit lui être passée lors de son initialisation, mais de manière standardisée.
*   **Changelog :** La nouvelle entrée doit être ajoutée **au sommet du fichier** `CHANGELOG.md`.

---

#### **Tâches Détaillées :**

1.  **Corriger les Imports dans les Fichiers de Test et de Diagnostic :**
    *   **Ouvrez `test_api.py` :**
        *   Supprimez la ligne `from glpi_explorer.api.client import ApiClient` et les imports similaires.
        *   Remplacez-les par les imports corrects basés sur la structure du dossier `src` :
            ```python
            from api_client import ApiClient
            from config_manager import ConfigManager
            ```
        *   Assurez-vous que la manipulation du `sys.path` est correcte pour que ces imports fonctionnent.
    *   **Ouvrez `test_shell.py` :**
        *   Faites les mêmes corrections pour tous les imports qui proviennent de `src`.
    *   **Ouvrez `temp_cable_diagnostic.py` :**
        *   Ce fichier utilise déjà `sys.path.insert(0, './src')`, ce qui est une bonne approche. Vérifiez que les imports qui suivent (`from src.api_client ...`) sont corrects. S'ils le sont, laissez-le tel quel.

2.  **Harmoniser le Chargement des Commandes dans `src/shell.py` :**
    *   Ouvrez le fichier `src/shell.py`.
    *   Localisez la méthode `_load_commands`.
    *   **Simplifiez la logique d'instanciation :** Actuellement, elle stocke les classes, puis instancie au moment de l'exécution. Nous allons changer cela pour tout instancier au démarrage.
        ```python
        # DANS _load_commands
        ...
        class_name = ...
        command_class = getattr(module, class_name)
        
        # NE PAS stocker la classe : self.commands[command_name] = command_class
        
        # Instancier directement et stocker l'INSTANCE
        # Pour l'instant, passez None pour le cache, nous l'ajouterons plus tard.
        self.commands[command_name] = command_class(self.api_client, self.console) 
        ...
        ```
    *   **Gérez le cas spécial de `help` :** La commande `help` a besoin de la liste de toutes les autres commandes. Nous ne pouvons donc l'instancier qu'à la fin.
        *   Modifiez la boucle de chargement pour **exclure** `help_command.py`.
        *   **Après la boucle**, instanciez manuellement la commande `help` en lui passant le dictionnaire des commandes que vous venez de construire.
        ```python
        # DANS _load_commands, APRÈS la boucle for
        try:
            from src.commands.help_command import HelpCommand
            # On passe self.commands (le dictionnaire des autres commandes) à HelpCommand
            self.commands['help'] = HelpCommand(self.api_client, self.console, self.commands)
        except Exception as e:
            # ... gestion d'erreur ...
        ```
    *   **Simplifiez la boucle d'exécution `run()` :**
        *   Maintenant que `self.commands` contient des instances, l'exécution est directe :
        ```python
        # DANS la méthode run(), boucle while True
        # ...
        if command_name in self.commands:
            command_instance = self.commands[command_name] # Récupère directement l'instance
            command_instance.execute(args)
        # ...
        ```
    *   **Modifiez le `__init__` de `help_command.py`** pour accepter la carte des commandes.

---

#### **Livrable Final :**

1.  **Mise à jour du `CHANGELOG.md` :**
    *   Gemini, vous devez documenter le nettoyage des imports et la standardisation du chargement des commandes.

2.  **Archive du Projet :**
    *   Créez une archive `.tar.gz` de l'intégralité du répertoire `glpi-explorer/` mis à jour.
    *   Nommez l'archive : **`mission_7.1_deliverable.tar.gz`**.

---
*Fin du Prompt de Mission*
