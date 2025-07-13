### **PROMPT DE MISSION POUR MANUS**

**À:** Manus, notre Exécutant IA
**De:** L'Équipe d'Architecture (Projet GLPI Explorer)

---

#### **`## [MISSION 2.2.1] - Correction de Syntaxe dans le Shell`**

**Rôle et Mission :**
Votre rôle est celui d'un **Débogueur Python**. Votre mission est de corriger une `SyntaxError` critique dans le fichier `src/shell.py` qui empêche l'application de se lancer.

**Contexte :**
Le projet est basé sur le livrable de la Mission 2.2. L'introduction de la commande `list` a corrompu la structure du bloc `try...except` dans la boucle principale du shell, provoquant un crash au démarrage.

**Objectif Principal :**
Restaurer la structure `try...except` correcte dans la méthode `run()` de `src/shell.py` pour que l'application redevienne fonctionnelle.

---

#### **Base de Connaissances et Directives Permanentes :**

*   **Syntaxe Python :** Un bloc `try` doit impérativement être suivi d'au moins un bloc `except` ou un bloc `finally`.
*   **Changelog :** La nouvelle entrée de correction doit être ajoutée **au sommet du fichier** `CHANGELOG.md`.

---

#### **Tâches Détaillées :**

1.  **Corriger le fichier `src/shell.py`** :
    *   Ouvrez le fichier `src/shell.py`.
    *   Localisez la boucle principale `while True` dans la méthode `run()`.
    *   Identifiez le bloc `try` qui commence au début de la boucle.
    *   Assurez-vous que ce bloc `try` est correctement suivi par le bloc `except EOFError:`. Il est probable que ce bloc `except` ait été supprimé ou mal indenté.
    *   La structure finale doit ressembler à ceci :
        ```python
        # Dans la méthode run()
        while True:
            try:
                # TOUTE la logique de lecture et de traitement des commandes
                # (if not full_command, parts = ..., if command == "get", elif command == "list", else...)
                # ...
                # ...
                # La dernière ligne du try doit être le "else:" pour la commande inconnue
                else:
                    self.console.print(Panel(f"[bold red]Commande inconnue:[/bold red] '{command}'. Commandes supportées: get, list, exit, quit", title="[red]Erreur[/red]"))

            except EOFError:
                # Ce bloc doit être au même niveau d'indentation que le "try"
                if self.api_client:
                    self.api_client.close_session()
                break
        ```
    *   Vérifiez attentivement l'indentation de l'ensemble du bloc `try...except`.

---

#### **Livrable Final :**

1.  **Mise à jour du `CHANGELOG.md` :**
    *   Manus, vous devez documenter cette correction en ajoutant une nouvelle entrée en haut du fichier.

2.  **Archive du Projet :**
    *   Créez une archive `.tar.gz` de l'intégralité du répertoire `glpi-explorer/` corrigé.
    *   Nommez l'archive : **`mission_2.2.1_deliverable.tar.gz`**.

---
*Fin du Prompt de Mission*
