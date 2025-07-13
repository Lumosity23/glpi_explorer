### **PROMPT DE MISSION POUR MANUS**

**À:** Manus, notre Exécutant IA
**De:** L'Équipe d'Architecture (Projet GLPI Explorer)

---

#### **`## [MISSION 2.2] - Implémentation de la Commande "list"`**

**Rôle et Mission :**
Votre rôle est celui d'un **Développeur d'outils CLI**. Votre mission est d'introduire une nouvelle commande, `list <type>`, qui permettra aux utilisateurs de lister tous les équipements d'un type donné présents dans GLPI, avec une pagination par défaut.

**Contexte :**
Le projet est basé sur le livrable de la Mission 2.1. La commande `get` est maintenant fonctionnelle avec une syntaxe spécifiant le type. Nous allons ajouter une commande `list` sur le même principe.

**Objectif Principal :**
Permettre à l'utilisateur de taper `list computer` et de recevoir en retour une table `rich` affichant les 5 premiers ordinateurs trouvés, avec leur ID, nom et statut.

---

#### **Base de Connaissances et Directives Permanentes :**

*   **Nouvelle Commande :** La commande à implémenter est `list <type>`.
*   **Documentation de l'API GLPI (Pagination) :**
    *   Le endpoint `GET /apirest.php/{itemtype}/` permet de lister tous les objets d'un type.
    *   Pour contrôler la pagination, on utilise le paramètre de requête `range`.
    *   **Exemple :** `range=0-4` pour récupérer 5 éléments (du 0ème au 4ème).
    *   Pour cette mission, nous utiliserons une valeur par défaut codée en dur : `range=0-4`. Nous rendrons cela dynamique dans une mission future.
*   **Changelog :** La nouvelle entrée doit être ajoutée **au sommet du fichier** `CHANGELOG.md`.

---

#### **Tâches Détaillées :**

1.  **Mettre à jour `src/api_client.py` pour lister les items :**
    *   Créez une nouvelle méthode `list_items(self, itemtype, item_range="0-4")`.
    *   Cette méthode doit effectuer une requête `GET` vers le endpoint `f"{self.base_url}/{itemtype}/"`.
    *   Les `params` de la requête doivent inclure :
        *   `range`: la valeur de `item_range` (par défaut "0-4").
        *   `expand_dropdowns`: `"true"`.
    *   La méthode doit gérer les erreurs et retourner la liste des objets (`response.json()`) si la requête réussit, ou une liste vide en cas d'échec.

2.  **Mettre à jour `src/shell.py` pour gérer la nouvelle commande :**
    *   Dans la méthode `run()`, ajoutez un `elif command == "list":` à votre structure de contrôle.
    *   **Validez l'entrée :** La commande `list` nécessite un argument de type. Si `args` est vide, affichez une erreur d'utilisation.
    *   **Utilisez le mapping `TYPE_ALIASES`** que vous avez déjà créé pour traduire l'alias utilisateur (ex: "pc") en `itemtype` GLPI (ex: "Computer"). Si l'alias est inconnu, affichez une erreur.
    *   **Appelez l'API :**
        ```python
        # ...
        glpi_itemtype = self.TYPE_ALIASES.get(user_type_alias)
        if not glpi_itemtype:
            # ... erreur type inconnu
            continue
            
        with self.console.status(f"Liste des objets de type {glpi_itemtype}..."):
            items = self.api_client.list_items(glpi_itemtype)
        
        if not items:
            self.console.print(Panel(f"Aucun objet de type '{user_type_alias}' trouvé.", title="[yellow]Résultat[/yellow]"))
            continue
        ```
    *   **Affichez les résultats :**
        *   Créez une `rich.table.Table` avec des en-têtes clairs : "ID", "Nom", "Statut".
        *   Itérez sur la liste `items` retournée par l'API.
        *   Pour chaque `item` dans la liste, ajoutez une ligne à la table avec les valeurs de `item.get('id')`, `item.get('name')`, et `item.get('states_id')`.
        *   Affichez la table finale dans un `Panel`.

---

#### **Livrable Final :**

1.  **Mise à jour du `CHANGELOG.md` :**
    *   Manus, vous devez documenter les changements que vous avez effectués, en ajoutant une nouvelle entrée en haut du fichier.

2.  **Archive du Projet :**
    *   Créez une archive `.tar.gz` de l'intégralité du répertoire `glpi-explorer/` mis à jour.
    *   Nommez l'archive : **`mission_2.2_deliverable.tar.gz`**.

---
*Fin du Prompt de Mission*

Une fois cette base fonctionnelle, nous nous attaquerons à la partie la plus intéressante : l'analyse des arguments comme `-n10` et `-na`.
