### **PROMPT DE MISSION POUR MANUS**

**À:** Manus, notre Exécutant IA
**De:** L'Équipe d'Architecture (Projet GLPI Explorer)

---

#### **`## [MISSION 1.4] - Fiabilisation du Chargement de la Configuration`**

**Rôle et Mission :**
Votre rôle est celui d'un Ingénieur en Fiabilité Logicielle (SRE). Votre mission est de rendre le processus de démarrage de l'application robuste en validant la configuration chargée, afin d'éviter les crashs ou les erreurs dus à un fichier de configuration existant mais invalide.

**Contexte :**
Le projet est basé sur le livrable de la Mission 1.3. L'application échoue à la connexion si un fichier `config.json` existe mais est incomplet (par exemple, contient des valeurs `null`).

**Objectif Principal :**
Modifier la logique de démarrage dans `src/shell.py` pour que l'application vérifie non seulement l'existence de la configuration, mais aussi sa validité (présence et contenu des clés nécessaires). Si la configuration est invalide, l'assistant de configuration interactif doit être lancé, comme si le fichier n'existait pas.

---

#### **Base de Connaissances et Directives Permanentes :**

*   **Configuration Valide :** Une configuration est considérée comme valide si c'est un dictionnaire contenant les clés `"url"`, `"app_token"`, `"user_token"`, et si aucune de leurs valeurs n'est vide ou `None`.
*   **Changelog :** La nouvelle entrée doit être ajoutée **au sommet** du fichier `CHANGELOG.md`.

---

#### **Tâches Détaillées :**

1.  **Mettre à jour `src/shell.py`** :
    *   Localisez la section de démarrage dans la méthode `run()`.
    *   Remplacez la simple vérification `if config is None:` par une logique de validation plus complète.
    *   **Créez une fonction d'aide privée** dans la classe `GLPIExplorerShell`, par exemple `_is_config_valid(self, config)` :
        ```python
        def _is_config_valid(self, config):
            if not isinstance(config, dict):
                return False
            required_keys = ["url", "app_token", "user_token"]
            for key in required_keys:
                if key not in config or not config[key]:
                    return False
            return True
        ```
    *   **Utilisez cette fonction d'aide** dans la méthode `run()` :
        ```python
        # Dans la méthode run()
        config_manager = ConfigManager()
        config = config_manager.load_config()

        if not self._is_config_valid(config):
            # Si la config n'est pas valide (ou n'existe pas), lancer le setup
            self.console.print(Panel("[bold blue]Bienvenue... ou la configuration est invalide.[/bold blue]\n...", expand=False))
            # ... reste de la boucle de configuration ...
        
        # Le reste du code continue ici...
        ```
    *   Assurez-vous que le message affiché à l'utilisateur est clair, qu'il s'agisse d'un premier lancement ou d'une configuration invalide.

---

#### **Livrable Final :**

1.  **Mise à jour du `CHANGELOG.md` :** Vous devez ajouter une **nouvelle entrée au sommet du fichier** :
    ```markdown
    ## [MISSION 1.4] - 2024-07-05 - par Manus

    ### Objectif de la Phase
    Fiabiliser le chargement de la configuration pour gérer les fichiers corrompus ou incomplets.

    ### Modifications Apportées
    - **`src/shell.py`**: Refonte de la logique de démarrage. L'application ne vérifie plus seulement l'existence du fichier de configuration, mais aussi sa validité (présence et contenu des clés `url`, `app_token`, `user_token`). Si la configuration est invalide, l'assistant de configuration est automatiquement relancé. Ajout d'une méthode d'aide privée `_is_config_valid` pour encapsuler cette logique.
    ```
2.  **Archive du Projet :**
    *   Créez une archive `.tar.gz` de l'intégralité du répertoire `glpi-explorer/` mis à jour.
    *   Nommez l'archive : **`mission_1.4_deliverable.tar.gz`**.

---
*Fin du Prompt de Mission*
