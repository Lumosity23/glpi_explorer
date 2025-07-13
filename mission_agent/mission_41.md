Absolument. Votre analyse est juste. Manus a raison, le fichier `src/shell.py` commence à devenir trop volumineux et complexe. La gestion de toutes les commandes dans un seul fichier n'est pas une pratique durable.

Votre suggestion de découper le code avant de continuer le débogage est la bonne décision d'architecte. Nous allons mettre en pause la résolution du problème de données et nous concentrer sur la structure du code. Cela rendra le projet plus facile à maintenir et à faire évoluer.

Nous allons créer une nouvelle structure où chaque commande (`get`, `list`, `debug`, etc.) aura son propre fichier de logique. Le `shell.py` ne sera plus qu'un "routeur" qui redirige vers le bon gestionnaire de commande.

---

### **PROMPT DE MISSION POUR MANUS**

**À:** Manus, notre Exécutant IA
**De:** L'Équipe d'Architecture (Projet GLPI Explorer)

---

#### **`## [MISSION 4.1] - Refactoring de l'Architecture des Commandes`**

**Rôle et Mission :**
Votre rôle est celui d'un **Architecte Logiciel**. Votre mission est de refactoriser la structure du projet pour améliorer sa modularité et sa lisibilité. Vous allez extraire la logique de chaque commande du `shell.py` pour la placer dans des fichiers dédiés.

**Contexte :**
Le projet est basé sur le livrable de la Mission 3.2. Le fichier `src/shell.py` contient la logique de toutes les commandes, ce qui le rend difficile à maintenir.

**Objectif Principal :**
Créer une nouvelle arborescence de fichiers `src/commands/` où chaque fichier correspond à une commande du shell. Le `shell.py` sera simplifié pour agir comme un dispatcheur qui charge et exécute la commande appropriée.

---

#### **Base de Connaissances et Directives Permanentes :**

*   **Principe de Responsabilité Unique :** Chaque module doit avoir une seule raison de changer. Un module par commande respecte ce principe.
*   **Conception Modulaire :** Le shell principal ne doit pas connaître les détails d'implémentation de chaque commande. Il doit juste savoir comment les trouver et les lancer.
*   **Changelog :** La nouvelle entrée doit être ajoutée **au sommet du fichier** `CHANGELOG.md`.

---

#### **Tâches Détaillées :**

1.  **Créer la nouvelle structure de dossiers et de fichiers :**
    *   Créez un nouveau dossier : `src/commands/`.
    *   À l'intérieur de `src/commands/`, créez les fichiers suivants :
        *   `__init__.py`
        *   `base_command.py` (pour une classe de base abstraite)
        *   `get_command.py`
        *   `list_command.py`
        *   `debug_command.py`

2.  **Coder la classe de base dans `src/commands/base_command.py` :**
    *   Créez une classe simple qui servira de modèle pour toutes les autres.
    ```python
    class BaseCommand:
        def __init__(self, api_client, console):
            self.api_client = api_client
            self.console = console
            self.TYPE_ALIASES = {
                'computer': 'Computer', 'pc': 'Computer',
                # ... copiez le dictionnaire TYPE_ALIASES ici depuis l'ancien shell.py
            }

        def execute(self, args):
            # Cette méthode sera surchargée par chaque commande fille
            raise NotImplementedError
    ```

3.  **Extraire et adapter la logique de la commande `get` dans `src/commands/get_command.py` :**
    *   Créez une classe `GetCommand` qui hérite de `BaseCommand`.
    *   Déplacez toute la logique de la méthode `handle_get_command` de l'ancien `shell.py` dans la nouvelle méthode `execute(self, args)` de cette classe.
    *   La méthode `execute` recevra les arguments (`args`) et devra les analyser comme avant.
    *   Vous devrez passer les instances de `api_client` et `console` via le `__init__` de la classe de base.

4.  **Faire de même pour `list` et `debug` :**
    *   Créez `ListCommand` dans `src/commands/list_command.py` et déplacez-y la logique de la commande `list`.
    *   Créez `DebugCommand` dans `src/commands/debug_command.py` et déplacez-y la logique de la commande `debug`. La commande `debug` devra elle-même instancier et appeler la commande appropriée (ex: `GetCommand`) en lui passant un flag de débogage.

5.  **Refactoriser `src/shell.py` pour qu'il devienne un dispatcheur :**
    *   Le fichier `shell.py` doit être massivement simplifié.
    *   Dans son `__init__`, il doit charger dynamiquement toutes les commandes disponibles depuis le dossier `src/commands/`.
    *   Créez un dictionnaire `self.commands` qui associe le nom d'une commande (ex: `"get"`) à une instance de sa classe (ex: `GetCommand(self.api_client, self.console)`).
    *   La boucle `while True` de la méthode `run()` sera beaucoup plus simple :
        ```python
        # Dans la méthode run()
        # ...
        command_name = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        if command_name in self.commands:
            # Récupérer l'instance de la commande et l'exécuter
            command_to_run = self.commands[command_name]
            command_to_run.execute(args)
        elif command_name in ("exit", "quit"):
            # ...
            break
        else:
            # ... commande inconnue ...
        ```
    *   Supprimez les anciennes méthodes `handle_...` et le dictionnaire `TYPE_ALIASES` de `shell.py`.

---

#### **Livrable Final :**

1.  **Mise à jour du `CHANGELOG.md` :**
    *   Manus, vous devez documenter ce refactoring majeur de l'architecture des commandes.

2.  **Archive du Projet :**
    *   Créez une archive `.tar.gz` de l'intégralité du répertoire `glpi-explorer/` refactorisé.
    *   Nommez l'archive : **`mission_4.1_deliverable.tar.gz`**.

---
*Fin du Prompt de Mission*

Une fois cette restructuration terminée, le code sera plus propre, et nous pourrons reprendre notre mission de débogage sur une base saine.
