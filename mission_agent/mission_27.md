### **PROMPT DE MISSION POUR MANUS**

**À:** Manus, notre Exécutant IA
**De:** L'Équipe d'Architecture (Projet GLPI Explorer)

---

#### **`## [MISSION 2.7] - Création d'un Script de Test API Autonome`**

**Rôle et Mission :**
Votre rôle est celui d'un **Ingénieur QA / Testeur d'API**. Votre mission est de créer un script Python autonome et non-interactif qui se connecte à l'API GLPI et exécute une série de tests prédéfinis pour diagnostiquer nos problèmes de recherche et de listing. Le script doit utiliser la configuration existante et produire des logs clairs.

**Contexte :**
Le projet est basé sur le livrable de la Mission 2.6. Nous n'arrivons pas à lister les `PassiveDevice` ni à utiliser la commande `get`. Nous avons besoin d'un outil de diagnostic pour isoler les problèmes de communication avec l'API, indépendamment du shell interactif.

**Objectif Principal :**
Créer un fichier `test_api.py` à la racine du projet. Ce script, une fois exécuté, devra :
1.  Charger la configuration depuis `~/.config/glpi-explorer/config.json`.
2.  Se connecter à l'API GLPI.
3.  Tenter de lister des objets pour une série d'itemtypes potentiels (y compris des variations de `PassiveDevice`).
4.  Tenter de rechercher un objet spécifique (ex: "PC1").
5.  Afficher des résultats de succès ou d'échec très clairs pour chaque test.
6.  Fermer la session proprement à la fin.

---

#### **Base de Connaissances et Directives Permanentes :**

*   **Autonomie du Script :** Le script ne doit nécessiter aucune interaction utilisateur.
*   **Clarté des Logs :** Utilisez `rich.console` pour formater la sortie et la rendre très lisible, en utilisant des couleurs pour les succès (vert) et les échecs (rouge).
*   **Liste d'Itemtypes à Tester :** Nous allons essayer plusieurs noms possibles pour les équipements passifs :
    *   `PassiveDevice`
    *   `PassiveEquipment`
    *   `PDU`
    *   `Rack`
    *   `Enclosure`
    *   `Cable`
*   **Changelog :** La nouvelle entrée doit être ajoutée **au sommet du fichier** `CHANGELOG.md`.

---

#### **Tâches Détaillées :**

1.  **Créer le fichier `test_api.py` à la racine du projet `glpi-explorer/`**.

2.  **Coder le script `test_api.py`** :
    *   **Imports :** Importez `ApiClient`, `ConfigManager`, et les composants `rich` (`Console`, `Panel`, `Rule`).
    *   **Structure principale :** Le script doit être contenu dans une structure `if __name__ == "__main__":`.
    *   **Initialisation :**
        *   Instanciez `console = Console()`.
        *   Affichez un titre, par ex: `console.rule("[bold cyan]Lancement du Script de Test API GLPI[/bold cyan]")`.
        *   Instanciez `config_manager = ConfigManager()` et chargez la configuration. Si la configuration n'est pas valide, affichez une erreur et quittez.
        *   Instanciez `api_client = ApiClient(config)`.
    *   **Connexion :**
        *   Essayez de vous connecter avec `api_client.connect()`. En cas d'échec, affichez une erreur fatale et quittez.
        *   Affichez un message de succès si la connexion réussit.
    *   **Définir les tests :**
        *   **Test 1 : Listing des Itemtypes.**
            *   Créez une liste `itemtypes_to_test = ['Computer', 'NetworkEquipment', 'PassiveDevice', 'PassiveEquipment', 'PDU', 'Rack', 'Enclosure', 'Cable']`.
            *   Affichez un séparateur : `console.rule("Test 1: Listing des 5 premiers objets par itemtype")`.
            *   Itérez sur cette liste. Pour chaque `itemtype` :
                *   Appelez `items = api_client.list_items(itemtype)`.
                *   Si `items` n'est pas une liste vide, affichez `[green]SUCCÈS[/green] - {len(items)} objets trouvés pour l'itemtype '{itemtype}'`.
                *   Sinon, affichez `[yellow]ÉCHEC/VIDE[/yellow] - Aucun objet trouvé ou itemtype invalide pour '{itemtype}'`.
        *   **Test 2 : Recherche d'un objet spécifique.**
            *   Affichez un séparateur : `console.rule("Test 2: Recherche de 'PC1' via search_item")`.
            *   Appelez `item_id = api_client.search_item('Computer', 'PC1')`.
            *   Si `item_id` n'est pas `None`, affichez `[green]SUCCÈS[/green] - 'PC1' trouvé avec l'ID: {item_id}`.
            *   Si `item_id` est `None`, affichez `[bold red]ÉCHEC[/bold red] - La recherche de 'PC1' a échoué.`.
    *   **Déconnexion :**
        *   Utilisez un bloc `finally` pour garantir que `api_client.close_session()` est appelé, que les tests aient réussi ou non.

---

#### **Livrable Final :**

1.  **Mise à jour du `CHANGELOG.md` :**
    *   Manus, vous devez documenter la création de ce nouveau script de test en ajoutant une nouvelle entrée en haut du fichier.

2.  **Archive du Projet :**
    *   Créez une archive `.tar.gz` de l'intégralité du répertoire `glpi-explorer/` mis à jour, qui inclut maintenant le nouveau fichier `test_api.py`.
    *   Nommez l'archive : **`mission_2.7_deliverable.tar.gz`**.

---
*Fin du Prompt de Mission*
