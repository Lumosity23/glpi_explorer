### **PROMPT DE MISSION POUR MANUS**

**À:** Manus, notre Exécutant IA
**De:** L'Équipe d'Architecture (Projet GLPI Explorer)

---

#### **`## [MISSION 2.6] - Débogage des Commandes "list" et "get"`**

**Rôle et Mission :**
Votre rôle est celui d'un **Ingénieur de Débogage**. Votre mission est de diagnostiquer et de corriger deux bugs critiques : l'échec de la commande `list` pour les équipements passifs et l'échec persistant de la commande `get`.

**Contexte :**
Le projet est basé sur le livrable de la Mission 2.5. `list` fonctionne pour les ordinateurs mais pas pour les patch panels. `get` ne trouve aucun objet.

**Objectif Principal :**
1.  Rendre la commande `list` fonctionnelle pour tous les types d'alias, y compris `patchpanel`, `wo`, etc.
2.  Rendre la commande `get` enfin fonctionnelle, capable de trouver un objet par son type et son nom.

---

#### **Base de Connaissances et Directives Permanentes :**

*   **Itemtypes GLPI :** Les noms des types dans l'API peuvent être sensibles à la casse et spécifiques. Il faut être précis. Il est possible que pour certains alias, nous n'utilisions pas le bon nom de classe GLPI.
*   **Débogage :** Pour comprendre ce qui se passe, nous allons temporairement ajouter des impressions (`print`) dans `api_client.py` pour inspecter les réponses brutes de l'API.
*   **Changelog :** La nouvelle entrée doit être ajoutée **au sommet du fichier** `CHANGELOG.md`.

---

#### **Tâches Détaillées :**

1.  **Corriger le bug de `list PassiveDevice` dans `src/shell.py`** :
    *   Ouvrez le fichier `src/shell.py`.
    *   Localisez le dictionnaire `self.TYPE_ALIASES`.
    *   **Hypothèse de correction :** Il est très probable que l'`itemtype` pour les patch panels et wall outlets ne soit pas `PassiveDevice` mais un autre nom. Essayons avec `PassiveEquipment` qui est un nom de classe plus courant dans GLPI pour ce genre d'équipement.
    *   **Modifiez les mappings suivants :**
        *   `'patchpanel': 'PassiveDevice'` -> `'patchpanel': 'PassiveEquipment'`
        *   `'patch': 'PassiveDevice'` -> `'patch': 'PassiveEquipment'`
        *   `'pp': 'PassiveDevice'` -> `'pp': 'PassiveEquipment'`
        *   `'walloutlet': 'PassiveDevice'` -> `'walloutlet': 'PassiveEquipment'`
        *   `'wo': 'PassiveDevice'` -> `'wo': 'PassiveEquipment'`
    *   Si cela ne fonctionne pas, le problème est plus profond, mais c'est la correction la plus probable.

2.  **Déboguer et corriger la commande `get` dans `src/api_client.py`** :
    *   Ouvrez le fichier `src/api_client.py`.
    *   Localisez la méthode `search_item`.
    *   **Ajoutez une instruction de débogage** pour voir ce que l'API renvoie exactement. Juste après avoir reçu la réponse, avant de la traiter, ajoutez :
        ```python
        # Dans la méthode search_item, dans le bloc try:
        response = requests.get(f"{self.base_url}/search/{itemtype}", ...)
        response.raise_for_status()
        
        # LIGNE DE DÉBOGAGE À AJOUTER :
        print(f"DEBUG: Réponse JSON de la recherche pour {itemtype} '{item_name}': {response.json()}")

        data = response.json()
        # ... reste de l'analyse ...
        ```
    *   **Analyser le JSON de recherche :** L'ancien projet s'attendait à une clé `'data'`. Notre code actuel gère ce cas. Cependant, la documentation de GLPI montre parfois que la réponse de `/search` est une structure plus complexe avec les clés `'totalcount'`, `'count'`, et `'data'`. La structure de `'data'` elle-même peut être une liste de dictionnaires, où chaque dictionnaire a pour clés les ID des colonnes.
    *   **Refactorisez la logique d'extraction de l'ID** pour être plus robuste et gérer ce cas, qui est le plus courant :
        ```python
        # Remplacer la logique d'analyse du JSON par ceci :
        result = response.json()
        
        if result.get('totalcount', 0) > 0:
            # La réponse est une structure de recherche complète
            first_item_data = result['data'][0]
            # L'ID de l'item est la clé '2' si le premier champ affiché est le nom
            # et que le deuxième est l'ID. Pour être sûr, cherchons-le.
            # Mais la documentation indique que l'ID de l'item est la clé '1' quand on ne force rien.
            # L'ID du champ ID de l'item est 2. Confusant.
            # Le nom de l'item est le champ 2.
            # L'ID est le champ 1. Mais l'ID de l'item est 2, et le nom 1...
            # OK, simplifions. L'ID de l'item est la clé '2' dans la réponse de recherche.
            # Le nom est la clé '1'. C'est une convention étrange de GLPI.
            # D'après la doc: ID = champ 2, Nom = champ 1.
            item_id = first_item_data.get('2') # ID de l'item
            if item_id:
                return item_id
        ```
        **Correction de la Correction :** Après relecture de la doc GLPI, c'est l'inverse. **Champ ID = `2`**, **Champ Nom = `1`**. Donc si on cherche par nom (champ 1), l'ID (champ 2) sera dans la réponse.
        ```python
        # Version finale et correcte de l'analyse
        result = response.json()
        if result.get('totalcount', 0) > 0:
            first_item_data = result['data'][0]
            item_id = first_item_data.get('2') # '2' est l'ID du champ "ID" de l'objet
            if item_id:
                return item_id
        ```
        *Cette logique est plus susceptible de fonctionner avec les versions modernes de l'API GLPI.*
        **Retirez la ligne de `print` de débogage avant de finaliser.**

---

#### **Livrable Final :**

1.  **Mise à jour du `CHANGELOG.md` :**
    *   Manus, vous devez documenter la correction de ces deux bugs en ajoutant une nouvelle entrée en haut du fichier.

2.  **Archive du Projet :**
    *   Créez une archive `.tar.gz` de l'intégralité du répertoire `glpi-explorer/` corrigé.
    *   Nommez l'archive : **`mission_2.6_deliverable.tar.gz`**.

---
*Fin du Prompt de Mission*

Une fois que `get` fonctionnera, nous nous attaquerons à la grande refonte de l'architecture que vous avez proposée.
