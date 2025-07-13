---

### **PROMPT DE MISSION POUR MANUS**

**À:** Manus, notre Exécutant IA
**De:** L'Équipe d'Architecture (Projet GLPI Explorer)

---

#### **`## [MISSION 0.3] - Configuration Interactive et Connexion API Persistante`**

**Rôle et Mission :**
Votre rôle est celui d'un **Développeur Python spécialisé en applications CLI robustes**. Votre mission est de transformer la gestion de la configuration de l'outil. Au lieu d'un fichier `.env`, vous implémenterez un processus de configuration interactif au premier lancement, qui sauvegardera les informations pour les sessions futures.

**Contexte :**
Le projet est basé sur l'archive `mission_0.1_deliverable.tar.gz` (nous repartons de la base du shell, car la logique de la Mission 0.2 est entièrement remplacée). Vous allez créer de nouveaux modules pour gérer la configuration persistante et la connexion API.

**Objectif Principal :**
Au lancement, l'application vérifie si un fichier de configuration existe. S'il n'existe pas, elle guide l'utilisateur à travers une série de questions pour obtenir l'URL de l'API et les tokens, teste la connexion, puis sauvegarde ces informations. Lors des lancements suivants, elle utilise directement les informations sauvegardées pour se connecter.

---

#### **Tâches Détaillées :**

1.  **Mettre à jour la structure du projet** pour refléter la nouvelle approche. Supprimez le `.env.example` et ajoutez les fichiers suivants :
    ```
    glpi-explorer/
    └── src/
        ├── api_client.py    # (Nouveau fichier)
        └── config_manager.py # (Nouveau fichier, remplace config.py)
    ```

2.  **Mettre à jour `requirements.txt`** avec la dépendance `requests` :
    ```
    rich
    requests 
    # python-dotenv n'est plus nécessaire
    ```

3.  **Coder le gestionnaire de configuration `src/config_manager.py`** :
    *   Importez `os`, `json`, `Path` de `pathlib`, et `Console`, `Panel`, `Prompt` de `rich`.
    *   Créez une classe `ConfigManager`.
    *   L'`__init__` doit définir le chemin du fichier de configuration, par exemple : `self.config_path = Path.home() / ".config" / "glpi-explorer" / "config.json"`.
    *   Créez une méthode `load_config(self)` :
        *   Elle vérifie si `self.config_path` existe.
        *   Si oui, elle lit le fichier JSON, charge les données (`url`, `app_token`, `user_token`) et les retourne dans un dictionnaire.
        *   Si non, elle retourne `None`.
    *   Créez une méthode `save_config(self, config_data)` :
        *   Elle s'assure que le répertoire parent (`~/.config/glpi-explorer/`) existe (`os.makedirs(..., exist_ok=True)`).
        *   Elle écrit le dictionnaire `config_data` dans `self.config_path` au format JSON.
    *   Créez une méthode `run_setup_interactive(self)` :
        *   Elle utilise `rich.prompt.Prompt.ask` pour demander à l'utilisateur :
            1.  L'URL de l'API GLPI (ex: `Prompt.ask("Veuillez entrer l'URL de l'API GLPI")`).
            2.  L'App-Token.
            3.  Le User-Token.
        *   Elle retourne un dictionnaire avec les données collectées.

4.  **Coder le client API `src/api_client.py`** :
    *   Créez une classe `ApiClient`.
    *   L'`__init__(self, config)` doit accepter un dictionnaire de configuration en paramètre et le stocker.
    *   Créez une méthode `connect(self)` qui utilise la configuration stockée pour tenter la connexion (similaire à la Mission 0.2). Elle doit retourner un tuple `(bool, str)` : `(True, session_token)` en cas de succès, et `(False, error_message)` en cas d'échec.
    *   La méthode `close_session(self, session_token)` doit accepter le `session_token` en paramètre pour fermer la session.

5.  **Mettre à jour `src/shell.py` (Logique principale)** :
    *   Importez `ConfigManager`, `ApiClient`, et les composants `rich`.
    *   Dans la méthode `run()` de `GLPIExplorerShell`:
        *   Instanciez `config_manager = ConfigManager()`.
        *   Appelez `config = config_manager.load_config()`.
        *   **Si `config` est `None` (premier lancement) :**
            *   Affichez un message de bienvenue expliquant que la configuration est nécessaire.
            *   Appelez `config = config_manager.run_setup_interactive()`.
            *   Instanciez `api_client_test = ApiClient(config)`.
            *   Testez la connexion : `is_connected, _ = api_client_test.connect()`.
            *   Si `is_connected` est `False`, affichez une erreur et redemandez la configuration (vous pouvez faire une boucle ici).
            *   Si `is_connected` est `True`, appelez `config_manager.save_config(config)` et affichez un message de succès.
        *   **Logique de connexion principale :**
            *   Instanciez `self.api_client = ApiClient(config)`.
            *   Utilisez `console.status()` pour vous connecter : `is_connected, session_token = self.api_client.connect()`.
            *   Si la connexion échoue, affichez une erreur et terminez.
            *   Si elle réussit, stockez le `session_token` dans une variable de la classe Shell (`self.session_token = session_token`).
            *   Affichez le panneau de bienvenue.
        *   Modifiez la gestion du `exit`/`quit` pour appeler `self.api_client.close_session(self.session_token)`.

---

#### **Base de Connaissances et Directives Permanentes :**

*   La configuration est maintenant **interactive** et **persistante**.
*   Le chemin de configuration `~/.config/glpi-explorer/config.json` est la convention à suivre sur les systèmes de type Unix.
*   Utilisez `rich.prompt.Prompt` pour toutes les demandes à l'utilisateur.

---

#### **Livrable Final :**

1.  **Mise à jour du `CHANGELOG.md` :** Vous devez ajouter une nouvelle entrée en haut de ce fichier :
    ```markdown
    ## [MISSION 0.3] - 2024-05-24 - par Manus

    ### Objectif de la Phase
    Remplacer la configuration par fichier .env par un processus de configuration interactif et persistant au premier lancement de l'application.

    ### Modifications Apportées
    - **`requirements.txt`**: Suppression de `python-dotenv`. `requests` est conservé.
    - **`src/config_manager.py`**: Création du module pour gérer la lecture, l'écriture et la collecte interactive des informations de configuration dans `~/.config/glpi-explorer/config.json`.
    - **`src/api_client.py`**: Mise à jour de la classe `ApiClient` pour qu'elle soit initialisée avec un dictionnaire de configuration et pour qu'elle retourne des informations plus détaillées sur l'échec/succès de la connexion.
    - **`src/shell.py`**: Refonte majeure de la logique de démarrage pour gérer le flux de configuration : vérifier si la configuration existe, lancer l'assistant interactif si nécessaire, tester et sauvegarder la configuration, puis se connecter à l'API.
    ```
2.  **Archive du Projet :**
    *   Créez une archive `.tar.gz` de l'intégralité du répertoire `glpi-explorer/` mis à jour.
    *   Nommez l'archive : **`mission_0.3_deliverable.tar.gz`**.

---
*Fin du Prompt de Mission*
