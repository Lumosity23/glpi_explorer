**Analyse des problèmes :**

1.  **`api_client.py` en double :** Le fichier contient deux définitions contradictoires de la classe `ApiClient`. La première est un vestige de la Mission 0.2 (basée sur des variables globales qui n'existent plus) et la seconde est la version correcte, mais la présence des deux crée une confusion et est une erreur de syntaxe.
2.  **Importation incorrecte dans `api_client.py` :** La première version de la classe importe `API_URL`, `APP_TOKEN` de `src.config_manager`, ce qui est incorrect. Ces variables ne sont pas définies dans ce module.
3.  **Gestion de la session de test :** Dans `shell.py`, la session de test est bien fermée, mais la logique pourrait être un peu plus claire et robuste.
4.  **Gestion des erreurs :** La méthode `connect` dans la deuxième (et correcte) version de `ApiClient` est bonne, mais on peut encore améliorer la clarté des messages d'erreur retournés à l'utilisateur.

Nous allons donc créer une **MISSION 0.3.1 - Correction et Fiabilisation**. Cette mission sera très ciblée pour que Manus corrige précisément ces points sans introduire de nouvelles fonctionnalités.

---

### **PROMPT DE MISSION POUR MANUS**

**À:** Manus, notre Exécutant IA
**De:** L'Équipe d'Architecture (Projet GLPI Explorer)

---

#### **`## [MISSION 0.3.1] - Correction et Fiabilisation de la Connexion API`**

**Rôle et Mission :**
Votre rôle est celui d'un **Développeur Python spécialiste du débogage et de la fiabilisation de code**. Votre mission est de corriger les erreurs critiques dans les fichiers de la mission précédente pour assurer un processus de configuration et de connexion stable et sans ambiguïté.

**Contexte :**
Le projet est basé sur le livrable de la Mission 0.3. Les fichiers `api_client.py` et `shell.py` contiennent des erreurs et des incohérences qui empêchent le bon fonctionnement de l'application.

**Objectif Principal :**
Corriger le code pour que le client API soit correctement défini, que la gestion de la configuration soit sans erreur, et que le processus de connexion et de déconnexion soit robuste.

---

#### **Tâches Détaillées :**

1.  **Corriger `src/api_client.py`** :
    *   **Supprimez complètement la première définition erronée de la classe `ApiClient`** et ses imports associés.
    *   Le fichier ne doit contenir **qu'une seule** définition de la classe `ApiClient`.
    *   Assurez-vous que la classe `ApiClient` restante est bien celle qui accepte `config` dans son constructeur `__init__`.
    *   Dans la méthode `connect`, améliorez la gestion des erreurs pour être plus spécifique. Modifiez le bloc `except` comme suit pour retourner des messages plus clairs :
        ```python
        except requests.exceptions.HTTPError as e:
            return False, f"Erreur HTTP : {e.response.status_code} - {e.response.reason}"
        except requests.exceptions.ConnectionError:
            return False, f"Erreur de connexion. Impossible de joindre l'URL : {self.base_url}"
        except requests.exceptions.RequestException as e:
            return False, f"Erreur de requête non spécifiée : {e}"
        ```
    *   Dans la méthode `close_session`, ajoutez un `try...except` pour gérer les erreurs de déconnexion silencieusement, mais assurez-vous de n'imprimer une erreur que si nécessaire (ou de ne rien faire, ce qui est acceptable).

2.  **Corriger `src/config_manager.py`** :
    *   Aucun changement majeur, mais pour la propreté, assurez-vous que les imports inutiles (`Panel`) sont retirés s'ils ne sont pas utilisés directement dans cette classe (ils le sont, donc c'est bon). La classe actuelle est fonctionnelle.

3.  **Améliorer `src/shell.py`** :
    *   Dans la boucle de configuration interactive, la logique pour fermer la session de test est correcte mais peut être simplifiée. Assurez-vous que le code ressemble à ceci pour plus de clarté :
        ```python
        # ... à la fin de la boucle de configuration
        if is_connected:
            test_session_token = message # message contient le token ici
            # Fermer la session de test immédiatement pour ne pas laisser de token orphelin
            api_client_test.close_session(test_session_token)
            
            config_manager.save_config(config)
            self.console.print(Panel("[bold green]Configuration sauvegardée avec succès ![/bold green]", title="[green]Succès[/green]"))
            break
        # ...
        ```
    *   Vérifiez que la méthode `close_session` est bien appelée avec le bon token (`self.session_token`) à la fin du programme. Le code actuel semble correct sur ce point, mais une double vérification est nécessaire.

4.  **Consolider le `CHANGELOG.md`** :
    *   Ne créez pas de nouvelle entrée de mission. Modifiez l'entrée existante de la `[MISSION 0.3]` pour y ajouter une note de correction. Ajoutez la ligne suivante à la fin de la section `### Modifications Apportées` :
        `- **Correction (Mission 0.3.1)**: Fiabilisation du client API, suppression du code en double, et amélioration de la gestion des erreurs de connexion.`

---

#### **Base de Connaissances et Directives Permanentes :**

*   **Clarté du code :** Éliminez tout code mort ou dupliqué.
*   **Robustesse :** La gestion des erreurs doit être explicite et fournir des retours utiles à l'utilisateur.
*   **Cohérence :** Le flux de données (config -> ApiClient -> shell) doit être logique et sans ambiguïté.

---

#### **Livrable Final :**

1.  **Mise à jour du `CHANGELOG.md` :** Vous devez modifier l'entrée `[MISSION 0.3]` comme spécifié ci-dessus.
2.  **Archive du Projet :**
    *   Créez une archive `.tar.gz` de l'intégralité du répertoire `glpi-explorer/` corrigé.
    *   Nommez l'archive : **`mission_0.3.1_deliverable.tar.gz`**.

---
*Fin du Prompt de Mission*
