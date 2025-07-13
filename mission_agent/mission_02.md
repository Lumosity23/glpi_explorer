---

### **PROMPT DE MISSION POUR MANUS**

**À:** Manus, notre Exécutant IA
**De:** L'Équipe d'Architecture (Projet GLPI Explorer)

---

#### **`## [MISSION 0.2] - Implémentation de la Connexion à l'API GLPI`**

**Rôle et Mission :**
Votre rôle est celui d'un **Développeur Python spécialisé en intégration d'API REST**. Votre mission est de doter "GLPI Explorer" de la capacité à s'authentifier auprès d'une instance GLPI au démarrage, en utilisant les informations de configuration fournies par l'utilisateur.

**Contexte :**
Le projet est basé sur l'archive `mission_0.1_deliverable.tar.gz`. Vous allez modifier les fichiers existants et en créer de nouveaux pour ajouter la logique de connexion. La structure des fichiers doit évoluer pour accueillir les nouveaux modules.

**Objectif Principal :**
Au lancement, l'application doit lire un fichier de configuration `.env`, tenter d'établir une session avec l'API GLPI, et afficher un message de succès ou d'échec avant de lancer le shell interactif.

---

#### **Tâches Détaillées :**

1.  **Mettre à jour la structure du projet** en ajoutant les fichiers suivants :
    ```
    glpi-explorer/
    ├── .env.example         # (Nouveau fichier)
    └── src/
        ├── api_client.py    # (Nouveau fichier)
        └── config.py        # (Nouveau fichier)
    ```

2.  **Créer le fichier d'exemple `.env.example`** :
    *   Ce fichier servira de modèle pour les utilisateurs.
    *   Il doit contenir les clés suivantes, sans valeurs :
        ```ini
        GLPI_API_URL="http://your-glpi-instance/apirest.php"
        GLPI_APP_TOKEN="your_app_token"
        GLPI_USER_TOKEN="your_user_token"
        ```

3.  **Coder le module de configuration `src/config.py`** :
    *   Importez `os` et `load_dotenv` de la librairie `dotenv`.
    *   Chargez les variables d'environnement depuis le fichier `.env` avec `load_dotenv()`.
    *   Définissez et exportez trois variables globales qui récupèrent les valeurs du `.env` : `API_URL`, `APP_TOKEN`, `USER_TOKEN`.
    *   Gérez le cas où une variable serait manquante en levant une `ValueError` avec un message clair (ex: "La variable d'environnement GLPI_API_URL est manquante.").

4.  **Coder le client API `src/api_client.py`** :
    *   Créez une classe nommée `ApiClient`.
    *   Importez `requests` (ajoutez-le aux `requirements.txt`) et les variables de configuration depuis `src/config.py`.
    *   L'`__init__` de la classe doit initialiser une variable d'instance `self.session_token` à `None`.
    *   Créez une méthode `connect(self)`. Cette méthode doit :
        *   Définir l'URL pour l'initialisation de la session : `f"{API_URL}/initSession"`.
        *   Préparer les `headers` de la requête :
            *   `'Content-Type': 'application/json'`
            *   `'App-Token': APP_TOKEN`
            *   `'Authorization': f'user_token {USER_TOKEN}'`
        *   Effectuer une requête `GET` vers l'URL avec `requests.get()`.
        *   Si la requête réussit (statut 200), extraire le `session_token` de la réponse JSON et le stocker dans `self.session_token`.
        *   Retourner `True` en cas de succès.
        *   Si la requête échoue (statut autre que 200 ou exception), ne pas lever d'erreur, mais retourner `False`.
    *   Créez une méthode `close_session(self)` qui, si `self.session_token` n'est pas `None`, effectue un `GET` vers `/killSession` pour fermer proprement la session.

5.  **Mettre à jour `src/shell.py`** :
    *   Importez `ApiClient` depuis `src/api_client.py` et `Panel`, `Console` depuis `rich`.
    *   Dans la méthode `run()` de `GLPIExplorerShell`:
        *   Juste avant d'afficher le panneau de bienvenue, instanciez `api_client = ApiClient()`.
        *   Utilisez `console.status()` pour afficher un message d'attente : `with console.status("[bold green]Connexion à l'API GLPI..."):`.
        *   À l'intérieur du `with`, appelez `is_connected = api_client.connect()`.
        *   **Après** le bloc `with`, vérifiez la valeur de `is_connected`.
            *   Si `False`, affichez un message d'erreur dans un `Panel` rouge (ex: `Panel("[bold red]Échec de la connexion.[/bold red] Veuillez vérifier votre configuration (.env) et l'accès à GLPI.", title="[red]Erreur[/red]")`) et terminez le programme.
            *   Si `True`, continuez et affichez le panneau de bienvenue comme avant.
    *   Modifiez la gestion du `exit`/`quit`. Avant de sortir de la boucle, appelez `api_client.close_session()` pour libérer le token sur le serveur GLPI.

6.  **Mettre à jour `requirements.txt`** en ajoutant la nouvelle dépendance :
    ```
    rich
    python-dotenv
    requests
    ```

---

#### **Base de Connaissances et Directives Permanentes :**

*   **Langage :** Python 3.9+
*   **Interface Utilisateur :** Continuez d'utiliser `rich` pour tous les outputs.
*   **Gestion des erreurs :** La connexion doit échouer gracieusement avec un message clair, sans traceback visible pour l'utilisateur.
*   **NE JAMAIS** coder d'identifiants en dur. Tout doit passer par le fichier `.env`.

---

#### **Livrable Final :**

1.  **Mise à jour du `CHANGELOG.md` :** Vous devez ajouter une nouvelle entrée en haut de ce fichier :
    ```markdown
    ## [MISSION 0.2] - 2024-05-24 - par Manus

    ### Objectif de la Phase
    Intégrer la logique de connexion à l'API REST de GLPI, en utilisant un fichier de configuration .env pour les identifiants et en gérant le cycle de vie de la session (init/kill).

    ### Modifications Apportées
    - **`.env.example`**: Création d'un fichier d'exemple pour les variables de configuration de l'API.
    - **`requirements.txt`**: Ajout de la dépendance `requests`.
    - **`src/config.py`**: Création du module pour charger et valider la configuration depuis le fichier `.env`.
    - **`src/api_client.py`**: Implémentation de la classe `ApiClient` avec les méthodes `connect()` et `close_session()`.
    - **`src/shell.py`**: Mise à jour du shell pour initier la connexion au démarrage, gérer les échecs et fermer la session en quittant.
    ```
2.  **Archive du Projet :**
    *   Créez une archive `.tar.gz` de l'intégralité du répertoire `glpi-explorer/` mis à jour.
    *   Nommez l'archive : **`mission_0.2_deliverable.tar.gz`**.

---
*Fin du Prompt de Mission*
