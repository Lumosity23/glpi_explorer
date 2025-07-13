### **PROMPT DE MISSION POUR MANUS**

**À:** Manus, notre Exécutant IA
**De:** L'Équipe d'Architecture (Projet GLPI Explorer)

---

#### **`## [MISSION 2.1] - Refonte de la Commande "get" avec Spécification de Type`**

**Rôle et Mission :**
Votre rôle est celui d'un **Architecte CLI**. Votre mission est de refondre la commande `get` pour qu'elle exige de l'utilisateur de spécifier le type d'objet à rechercher. Cela simplifiera la logique de recherche et augmentera la fiabilité des résultats.

**Contexte :**
Le projet est basé sur le livrable de la Mission 1.6. La recherche d'items échoue systématiquement. Nous changeons de stratégie pour demander à l'utilisateur de spécifier le type d'objet.

**Objectif Principal :**
Modifier l'application pour que la commande `get` fonctionne avec la syntaxe `get <type> <nom_objet>`. Par exemple : `get computer pc-01`. La recherche se fera alors uniquement sur le type `Computer`.

---

#### **Base de Connaissances et Directives Permanentes :**

*   **Nouvelle Syntaxe de Commande :** La commande `get` a maintenant deux arguments : le type et le nom.
*   **Mapping des Types :** Nous devons créer un mapping entre des alias simples que l'utilisateur peut taper et les `itemtypes` réels de GLPI. Voici le mapping initial :
    *   `computer`, `pc` -> `'Computer'`
    *   `switch`, `sw` -> `'NetworkEquipment'`
    *   `patchpanel`, `patch`, `pp` -> `'PassiveDevice'`
    *   `walloutlet`, `wo` -> `'PassiveDevice'`
    *   `hub`, `hb` -> `'NetworkEquipment'`
    *   `cable`, `cb` -> `'Cable'`
*   **Changelog :** La nouvelle entrée doit être ajoutée **au sommet du fichier** `CHANGELOG.md`.

---

#### **Tâches Détaillées :**

1.  **Mettre à jour `src/shell.py` pour la nouvelle syntaxe :**
    *   Dans la méthode `run()`, localisez la gestion de la commande `get`.
    *   La variable `args` contiendra maintenant le type et le nom (ex: `"computer pc-01"`). Vous devez la découper en deux parties.
    *   **Validez l'entrée :** Assurez-vous qu'il y a bien deux arguments après `get`. Si ce n'est pas le cas, affichez un message d'erreur clair expliquant la nouvelle syntaxe : `Usage: get <type> <nom_objet>`.
    *   Créez un dictionnaire pour le mapping des types en haut de votre classe `GLPIExplorerShell` ou dans une nouvelle classe/fichier de constantes si vous préférez.
        ```python
        self.TYPE_ALIASES = {
            'computer': 'Computer', 'pc': 'Computer',
            'switch': 'NetworkEquipment', 'sw': 'NetworkEquipment',
            # ... ajoutez les autres mappings ...
        }
        ```
    *   Récupérez le `itemtype` GLPI réel à partir de l'alias fourni par l'utilisateur. Si l'alias n'est pas valide, affichez une erreur.

2.  **Mettre à jour `src/api_client.py` pour simplifier la recherche :**
    *   La méthode `search_item_by_name` est maintenant trop complexe. Simplifiez-la.
    *   **Modifiez sa signature** pour qu'elle accepte `itemtype` et `item_name` : `search_item(self, itemtype, item_name)`.
    *   **Supprimez la boucle** qui itérait sur les différents types. La méthode ne doit plus faire qu'une seule requête sur l'`itemtype` fourni.
    *   La méthode doit retourner l'ID de l'item trouvé, ou `None` si non trouvé. Elle n'a plus besoin de retourner l'`itemtype` puisque nous le connaissons déjà.

3.  **Adapter l'appel dans `src/shell.py` :**
    *   Modifiez l'appel dans le bloc de la commande `get` pour utiliser la nouvelle méthode simplifiée :
        ```python
        # ...
        user_type_alias = args_parts[0]
        item_name = args_parts[1]
        
        glpi_itemtype = self.TYPE_ALIASES.get(user_type_alias)
        if not glpi_itemtype:
            # Affichez une erreur "Type inconnu"
            continue
            
        with self.console.status(f"Recherche de {item_name} ({glpi_itemtype})..."):
            item_id = self.api_client.search_item(glpi_itemtype, item_name)

        if item_id is None:
            # ... affichez "Non trouvé"
        else:
            # ... récupérez les détails avec glpi_itemtype et item_id
        # ...
        ```

---

#### **Livrable Final :**

1.  **Mise à jour du `CHANGELOG.md` :**
    *   Manus, vous devez documenter les changements que vous avez effectués dans ce fichier, en ajoutant une nouvelle entrée en haut. Décrivez la refonte de la commande `get` et la nouvelle syntaxe requise.

2.  **Archive du Projet :**
    *   Créez une archive `.tar.gz` de l'intégralité du répertoire `glpi-explorer/` mis à jour.
    *   Nommez l'archive : **`mission_2.1_deliverable.tar.gz`**.

---
*Fin du Prompt de Mission*

Cette approche est un pivot stratégique important. En forçant l'utilisateur à être plus précis, nous réduisons la complexité et les sources d'erreurs potentielles de notre côté. C'est un excellent pas en avant pour la robustesse de l'outil.
