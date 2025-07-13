### **PROMPT DE MISSION POUR MANUS**

**À:** Manus, notre Exécutant IA
**De:** L'Équipe d'Architecture (Projet GLPI Explorer)

---

#### **`## [MISSION 1.3] - Refactoring et Correction du Client API`**

**Rôle et Mission :**
Votre rôle est celui d'un **Ingénieur Logiciel Senior**. Votre mission est de refactoriser la classe `ApiClient` pour qu'elle soit propre, cohérente et qu'elle gère son état interne (le `session_token`) correctement. Cela corrigera le bug qui empêche la commande `get` de fonctionner.

**Contexte :**
Le projet est basé sur le livrable de la Mission 1.2. Le fichier `src/api_client.py` est corrompu avec des définitions de fonctions en double et une mauvaise structure de classe. La gestion du `session_token` est défaillante.

**Objectif Principal :**
Nettoyer `src/api_client.py` pour n'avoir qu'une seule classe `ApiClient` bien structurée. La classe doit stocker le `session_token` après une connexion réussie et l'utiliser automatiquement pour toutes les requêtes suivantes, sans avoir besoin de le passer en paramètre à chaque fois.

---

#### **Base de Connaissances et Directives Permanentes :**

*   **Conception de Classe (POO) :** Un objet client (`ApiClient`) doit maintenir son propre état. Une fois connecté, il doit "se souvenir" de son `session_token` et l'utiliser pour toutes ses autres méthodes. C'est le principe de l'encapsulation.
*   **Nouvelle Directive Architecturale :** Les nouvelles entrées dans `CHANGELOG.md` doivent être ajoutées **au sommet du fichier**.

---

#### **Tâches Détaillées :**

1.  **Réécrire complètement `src/api_client.py`** :
    *   Effacez tout le contenu actuel du fichier.
    *   Recréez une **unique** classe `ApiClient`.
    *   L'`__init__(self, config)` doit initialiser :
        *   `self.config`, `self.base_url`, `self.app_token`, `self.user_token` comme avant.
        *   Ajoutez `self.session_token = None` pour stocker le token.
    *   La méthode `connect(self)` :
        *   Son but est maintenant de récupérer le token ET de le stocker dans l'objet.
        *   Si la connexion réussit, elle doit faire `self.session_token = session_token_recu` et retourner `True`.
        *   Si elle échoue, elle retourne `False`. Elle ne retourne plus le token lui-même.
    *   La méthode `close_session(self)` :
        *   Elle doit maintenant utiliser `self.session_token`.
        *   Elle n'a plus besoin de recevoir le token en paramètre.
    *   La méthode `search_item_by_name(self, item_name)` :
        *   Elle ne doit **plus** accepter `session_token` en paramètre.
        *   À l'intérieur, elle doit utiliser `self.session_token` pour construire les headers.
        *   Ajoutez une vérification au début : `if not self.session_token: return None, None`.
    *   La méthode `get_item_details(self, itemtype, item_id)` :
        *   Elle ne doit **plus** accepter `session_token` en paramètre.
        *   À l'intérieur, elle doit utiliser `self.session_token` pour construire les headers.
        *   Ajoutez une vérification au début : `if not self.session_token: return None`.

2.  **Mettre à jour `src/shell.py` pour s'adapter au nouveau `ApiClient`** :
    *   Dans la méthode `run()`, la logique de connexion change légèrement :
        ```python
        # ...
        self.api_client = ApiClient(config)
        with self.console.status("[bold green]Connexion à l'API GLPI...[/bold green]"):
            is_connected = self.api_client.connect() # Ne retourne plus le token

        if not is_connected:
            # ... gestion de l'erreur
            return
        # La connexion a réussi, le token est maintenant dans self.api_client.
        # Plus besoin de self.session_token dans la classe Shell.
        ```
    *   Supprimez l'attribut `self.session_token` de la classe `GLPIExplorerShell`. Il est maintenant géré par `self.api_client`.
    *   Dans la boucle `while True`, modifiez les appels à l'API :
        ```python
        # ...
        elif command == "get":
            # ...
            itemtype, item_id = self.api_client.search_item_by_name(item_name) # Plus besoin de passer le token
            # ...
            if itemtype:
                details = self.api_client.get_item_details(itemtype, item_id) # Plus besoin de passer le token
        # ...
        ```
    *   Modifiez la logique de `exit`/`quit` :
        ```python
        # ...
        if command in ("exit", "quit"):
            if self.api_client:
                self.api_client.close_session() # Plus besoin de passer le token
            break
        # ...
        ```
    *   **TRÈS IMPORTANT :** La logique de test de connexion lors de la configuration initiale doit aussi être adaptée.
        *   Le `api_client_test.connect()` va réussir et stocker le token. Il faut le fermer immédiatement.
        *   Modifiez le bloc de test de connexion pour ressembler à ceci :
        ```python
        # Dans la boucle de configuration interactive...
        api_client_test = ApiClient(config)
        with self.console.status("[bold green]Test de la connexion API...[/bold green]"):
            is_connected = api_client_test.connect()

        if not is_connected:
            # ... gestion de l'erreur ...
        else:
            api_client_test.close_session() # Ferme la session de test immédiatement
            config_manager.save_config(config)
            self.console.print(Panel("[bold green]Configuration sauvegardée avec succès ![/bold green]", title="[green]Succès[/green]"))
            break
        ```

---

#### **Livrable Final :**

1.  **Mise à jour du `CHANGELOG.md` :** Vous devez ajouter une **nouvelle entrée au sommet du fichier** :
    ```markdown
    ## [MISSION 1.3] - 2024-07-05 - par Manus

    ### Objectif de la Phase
    Refactoring du client API pour une gestion correcte et encapsulée du `session_token`.

    ### Modifications Apportées
    - **`src/api_client.py`**: Le fichier a été entièrement réécrit pour avoir une seule classe `ApiClient` propre. La classe gère maintenant son propre `session_token` en interne après une connexion réussie. Les méthodes n'ont plus besoin de recevoir le token en paramètre.
    - **`src/shell.py`**: Mise à jour de toute la logique pour s'adapter au nouveau `ApiClient`. Le `session_token` n'est plus géré par le shell mais par le client API. La logique de connexion, de test, d'appel des commandes et de déconnexion a été simplifiée.
    ```
2.  **Archive du Projet :**
    *   Créez une archive `.tar.gz` de l'intégralité du répertoire `glpi-explorer/` mis à jour.
    *   Nommez l'archive : **`mission_1.3_deliverable.tar.gz`**.

---
*Fin du Prompt de Mission*
