### **PROMPT DE MISSION POUR MANUS**

**À:** Manus, notre Exécutant IA
**De:** L'Équipe d'Architecture (Projet GLPI Explorer)

---

#### **`## [MISSION 0.1] - Création du Socle de l'Application CLI Interactive`**

**Rôle et Mission :**
Votre rôle est celui d'un **Développeur Python spécialiste des applications CLI modernes**. Votre mission est de créer la structure de base et la boucle interactive de notre outil "GLPI Explorer", en utilisant la librairie `rich` pour une expérience utilisateur soignée dès le départ.

**Contexte :**
Le projet démarre de zéro. Aucun fichier n'existe. Vous devez créer toute l'arborescence et le code initial.

**Objectif Principal :**
Créer une application Python qui, une fois lancée, affiche un message de bienvenue dans un panneau, présente un prompt interactif, attend une saisie utilisateur, et se termine proprement lorsque l'utilisateur tape `exit` ou `quit`.

---

#### **Tâches Détaillées :**

1.  **Créer la structure du projet** suivante :
    ```
    glpi-explorer/
    ├── .gitignore
    ├── CHANGELOG.md         # (Laissez-le vide, vous le remplirez à la fin)
    ├── requirements.txt
    ├── main.py
    └── src/
        ├── __init__.py
        └── shell.py
    ```

2.  **Remplir `requirements.txt`** avec les dépendances nécessaires pour cette mission :
    ```
    rich
    python-dotenv
    ```

3.  **Configurer `.gitignore`** avec des entrées Python standard pour ignorer les environnements virtuels, les caches et les fichiers de configuration locaux :
    ```
    __pycache__/
    *.pyc
    .venv/
    venv/
    .env
    ```

4.  **Coder le point d'entrée `main.py`** :
    *   Ce fichier doit être très simple.
    *   Il doit importer la future classe `GLPIExplorerShell` depuis `src/shell.py`.
    *   Il doit instancier cette classe et appeler sa méthode `run()`.

5.  **Coder le shell interactif `src/shell.py`** :
    *   Créez une classe nommée `GLPIExplorerShell`.
    *   Créez une méthode `run()` dans cette classe.
    *   Dans la méthode `run()` :
        *   Importez `Console` et `Panel` de la librairie `rich`.
        *   Instanciez `console = Console()`.
        *   Affichez un message de bienvenue stylisé à l'aide de `rich.panel.Panel`. Exemple : `console.print(Panel("Bienvenue dans GLPI Explorer", title="[bold cyan]GLPI Explorer[/]", subtitle="[green]v0.1[/]"))`.
        *   Démarrez une boucle infinie (`while True`).
        *   À l'intérieur de la boucle, utilisez `console.input()` pour afficher un prompt stylisé et récupérer la saisie de l'utilisateur. Le prompt doit être : `[bold cyan](glpi-explorer)> [/]`.
        *   Gérez le cas où l'utilisateur appuie sur `Ctrl+D` (`EOFError`) pour quitter proprement.
        *   Vérifiez si la commande entrée (après l'avoir passée en minuscules et sans espaces superflus) est `exit` ou `quit`. Si c'est le cas, sortez de la boucle.
        *   Pour toute autre commande, ne faites rien pour l'instant.
        *   Après la sortie de la boucle, affichez un message de départ simple, comme `console.print("[yellow]Au revoir ![/yellow]")`.

---

#### **Base de Connaissances et Directives Permanentes :**

*   **Langage :** Python 3.9+
*   **Interface Utilisateur :** La librairie `rich` est la **seule** autorisée pour toute interaction avec le terminal.
*   **Structure :** La structure de fichiers et de dossiers définie ci-dessus est **obligatoire**.
*   **NE JAMAIS** exécuter de commandes de gestion de paquets (`pip install`). Contentez-vous de définir les dépendances dans `requirements.txt`.
*   **NE JAMAIS** exécuter l'application. Votre rôle est d'écrire le code, pas de le lancer.

---

#### **Livrable Final :**

1.  **Mise à jour du `CHANGELOG.md` :** Vous devez ajouter une entrée en haut de ce fichier en suivant **strictement** ce format :
    ```markdown
    ## [MISSION 0.1] - 2024-05-24 - par Manus

    ### Objectif de la Phase
    Mise en place du socle de l'application CLI interactive, de sa structure de fichiers et de sa boucle de commande principale.

    ### Modifications Apportées
    - **`glpi-explorer/`**: Création de l'arborescence initiale du projet.
    - **`requirements.txt`**: Ajout des dépendances `rich` et `python-dotenv`.
    - **`.gitignore`**: Configuration initiale pour les projets Python.
    - **`main.py`**: Création du point d'entrée qui lance le shell interactif.
    - **`src/shell.py`**: Implémentation de la classe `GLPIExplorerShell` avec une boucle de commande, un message de bienvenue, un prompt stylisé et la logique pour quitter (`exit`/`quit`).
    ```
2.  **Archive du Projet :**
    *   Créez une archive `.tar.gz` de l'intégralité du répertoire `glpi-explorer/`.
    *   Nommez l'archive : **`mission_0.1_deliverable.tar.gz`**.

---
*Fin du Prompt de Mission*
