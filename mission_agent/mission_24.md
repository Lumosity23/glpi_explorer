### **PROMPT DE MISSION POUR MANUS**

**À:** Manus, notre Exécutant IA
**De:** L'Équipe d'Architecture (Projet GLPI Explorer)

---

#### **`## [MISSION 2.4] - Amélioration du Shell avec Historique des Commandes`**

**Rôle et Mission :**
Votre rôle est celui d'un **Développeur d'Expérience Utilisateur CLI**. Votre mission est de remplacer la méthode d'entrée utilisateur basique par une solution plus avancée qui offre l'historique des commandes (navigation avec les flèches haut/bas) et une meilleure expérience d'édition.

**Contexte :**
Le projet est basé sur le livrable de la Mission 2.3. L'application utilise `rich.console.Console.input()` pour lire les commandes, ce qui est simple mais ne fournit pas d'historique.

**Objectif Principal :**
Intégrer la librairie `prompt-toolkit` pour remplacer `console.input()`. Le shell doit permettre à l'utilisateur de rappeler les commandes précédemment tapées en utilisant les flèches directionnelles du clavier.

---

#### **Base de Connaissances et Directives Permanentes :**

*   **Nouvelle Dépendance :** Nous allons utiliser la librairie `prompt-toolkit`.
*   **Intégration :** `prompt-toolkit` peut être utilisé pour créer un "prompt" qui gère l'historique en mémoire. Il remplace l'appel à `console.input()`.
*   **Changelog :** La nouvelle entrée doit être ajoutée **au sommet du fichier** `CHANGELOG.md`.

---

#### **Tâches Détaillées :**

1.  **Mettre à jour `requirements.txt`** :
    *   Ajoutez la nouvelle dépendance. Le fichier doit maintenant contenir :
        ```
        rich
        requests
        prompt-toolkit
        ```

2.  **Mettre à jour `src/shell.py` pour intégrer `prompt-toolkit`** :
    *   **Ajoutez les imports nécessaires** en haut du fichier :
        ```python
        from prompt_toolkit import PromptSession
        from prompt_toolkit.history import InMemoryHistory
        from prompt_toolkit.formatted_text import FormattedText
        ```
    *   **Modifiez le constructeur `__init__`** de la classe `GLPIExplorerShell` :
        *   Créez une instance de l'historique : `self.history = InMemoryHistory()`
        *   Créez une session de prompt en lui passant l'historique : `self.prompt_session = PromptSession(history=self.history)`
    *   **Modifiez la boucle `while True` dans la méthode `run()`** :
        *   Localisez la ligne `full_command = self.console.input(...)`.
        *   **Remplacez cette ligne** par un appel à notre nouvelle session de prompt :
            ```python
            # Définir le message du prompt avec la syntaxe de prompt-toolkit
            prompt_message = FormattedText([
                ('bold cyan', '(glpi-explorer)> ')
            ])
            
            # Utiliser la session pour obtenir la commande
            full_command = self.prompt_session.prompt(prompt_message).strip()
            ```
        *   Le reste de la logique de la boucle (gestion de l'entrée vide, `split`, `if/elif` pour les commandes) n'a **pas besoin d'être modifié**. Le remplacement de `console.input` par `self.prompt_session.prompt` est la seule modification nécessaire dans la boucle. Le copier/coller et l'édition de ligne standard seront gérés automatiquement par `prompt-toolkit`.

---

#### **Livrable Final :**

1.  **Mise à jour du `CHANGELOG.md` :**
    *   Manus, vous devez documenter cette amélioration majeure de l'interface en ajoutant une nouvelle entrée en haut du fichier.

2.  **Archive du Projet :**
    *   Créez une archive `.tar.gz` de l'intégralité du répertoire `glpi-explorer/` mis à jour.
    *   Nommez l'archive : **`mission_2.4_deliverable.tar.gz`**.

---
*Fin du Prompt de Mission*
