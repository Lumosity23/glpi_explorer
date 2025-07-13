---

### **PROMPT DE MISSION (Révisé) POUR MANUS**

**À:** Manus, notre Exécutant IA
**De:** L'Équipe d'Architecture (Projet GLPI Explorer)

---

#### **`## [MISSION 1.1] - Implémentation de la Commande "get"`**

**Rôle et Mission :**
Votre rôle est celui d'un **Développeur Python spécialiste des CLI fonctionnels**. Votre mission est d'implémenter la première commande utilisateur, `get <nom_objet>`, qui permettra de rechercher un équipement dans GLPI par son nom et d'afficher ses informations de base.

**Contexte :**
Le projet est basé sur l'archive `mission_0.3.1_deliverable.tar.gz`. L'application peut maintenant se connecter à GLPI. Le shell est interactif mais ne traite aucune commande à part `exit` et `quit`.

**Objectif Principal :**
Permettre à l'utilisateur de taper `get pc-01` dans le shell et de voir en retour un panneau (`rich.panel.Panel`) contenant les informations de base de l'ordinateur "pc-01" récupérées depuis l'API GLPI.

---

#### **Base de Connaissances et Directives Permanentes :**

*   **Réponse utilisateur :** Toute sortie (succès ou erreur) doit être formatée à l'aide de `rich.panel.Panel` et/ou `rich.table.Table` pour une présentation propre.
*   **Gestion des erreurs :** Si une commande est mal formée (ex: `get` sans argument), l'outil doit afficher une aide et non crasher.

*   **Documentation de l'API GLPI pertinente pour cette mission :**

    *   **Pour rechercher un objet par son nom (`search_item_by_name`) :**
        *   **Endpoint :** `GET /apirest.php/search/:itemtype/`
        *   **Paramètres de requête (`params`) :** Vous devez utiliser des critères de recherche. Le format est `criteria[INDEX][key]=value`.
        *   Pour rechercher un objet par son nom, le critère est :
            *   `criteria[0][field]` doit être `2`. C'est l'ID du champ "Nom" (`name`) pour la plupart des `itemtype`.
            *   `criteria[0][searchtype]` doit être `equals`.
            *   `criteria[0][value]` doit être le nom de l'objet recherché.
        *   **Exemple de requête :** `GET /apirest.php/search/Computer?criteria[0][field]=2&criteria[0][searchtype]=equals&criteria[0][value]=pc-01`
        *   **Réponse :** La réponse contient une clé `"data"` qui est une liste d'objets correspondants. Vous ne devez traiter que le premier.

    *   **Pour récupérer les détails d'un objet (`get_item_details`) :**
        *   **Endpoint :** `GET /apirest.php/:itemtype/:id`
        *   **Paramètres de requête (`params`) :**
            *   `expand_dropdowns=true` : Pour obtenir les noms lisibles des champs (ex: "En production") au lieu de leurs IDs (ex: "1").
            *   `with_networkports=true` : Pour récupérer les informations sur les ports réseau, ce qui sera utile pour les missions futures.
        *   **Exemple de requête :** `GET /apirest.php/Computer/123?expand_dropdowns=true&with_networkports=true`

---

#### **Tâches Détaillées :**

1.  **Mettre à jour `src/api_client.py`** pour ajouter des méthodes de recherche :
    *   Ajoutez une nouvelle méthode `search_item_by_name(self, item_name)`.
        *   Cette méthode doit itérer sur une liste de types d'objets GLPI : `['Computer', 'NetworkEquipment', 'PassiveDevice']`.
        *   Pour chaque `itemtype`, elle doit effectuer une requête `GET` vers le endpoint de recherche (`/search/:itemtype/`) en utilisant les `params` décrits dans la base de connaissances. N'oubliez pas d'inclure le `Session-Token` dans les headers.
        *   Si la recherche trouve un ou plusieurs résultats (vérifiez que `response.json().get('data')` n'est pas vide), prenez le **premier résultat**, extrayez son `id` et retournez un tuple `(itemtype, item_id)`.
        *   Si, après avoir cherché dans tous les types, aucun objet n'est trouvé, la méthode doit retourner `(None, None)`.
        *   Gérez les erreurs de requête (par exemple, avec un bloc `try...except`).
    *   Ajoutez une nouvelle méthode `get_item_details(self, itemtype, item_id)`.
        *   Elle doit faire une requête `GET` vers `f"{self.base_url}/{itemtype}/{item_id}"` avec les `params` décrits dans la base de connaissances.
        *   Elle doit retourner le JSON complet de la réponse en cas de succès, ou `None` en cas d'échec.

2.  **Mettre à jour `src/shell.py`** pour gérer la nouvelle commande :
    *   Dans la boucle `while True` de la méthode `run()` :
        *   Analysez l'entrée utilisateur pour séparer la commande de sa cible (ex: `get pc-01`).
        *   Dans la structure de contrôle, si la commande est `"get"` :
            *   Validez qu'une cible a été fournie.
            *   Utilisez `console.status()` pour indiquer à l'utilisateur que la recherche est en cours.
            *   Appelez `search_item_by_name` pour obtenir l'ID et le type de l'objet.
            *   Si non trouvé, affichez un `Panel` d'erreur.
            *   Si trouvé, appelez `get_item_details`.
            *   Si les détails sont obtenus, créez une `Table` `rich` (sans en-tête ni bordure) pour afficher les paires clé/valeur importantes : "ID", "Nom", "Type GLPI", "Statut", "Localisation". Vous trouverez ces informations dans le JSON de réponse (`details.get('id')`, etc.).
            *   Encapsulez cette table dans un `Panel` final et affichez-le.

---

#### **Livrable Final :**

1.  **Mise à jour du `CHANGELOG.md` :**
    ```markdown
    ## [MISSION 1.1] - 2024-05-25 - par Manus

    ### Objectif de la Phase
    Implémenter la première commande fonctionnelle `get <nom_objet>` pour rechercher un équipement et afficher ses détails de base.

    ### Modifications Apportées
    - **`src/api_client.py`**: Ajout des méthodes `search_item_by_name` et `get_item_details` pour interagir avec les endpoints de recherche et de récupération d'items de GLPI, en se basant sur la documentation de l'API fournie.
    - **`src/shell.py`**: Mise à jour de la boucle principale pour analyser les commandes utilisateur. Implémentation de la logique pour la commande `get`, incluant la recherche, la récupération des détails et l'affichage formaté des résultats dans un `Panel` et une `Table` `rich`.
    ```
2.  **Archive du Projet :**
    *   Créez une archive `.tar.gz` de l'intégralité du répertoire `glpi-explorer/` mis à jour.
    *   Nommez l'archive : **`mission_1.1_deliverable.tar.gz`**.

---
*Fin du Prompt de Mission*
