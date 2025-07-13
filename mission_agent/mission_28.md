### **PROMPT DE MISSION POUR MANUS**

**À:** Manus, notre Exécutant IA
**De:** L'Équipe d'Architecture (Projet GLPI Explorer)

---

#### **`## [MISSION 2.8] - Correction de la Construction de la Requête de Recherche`**

**Rôle et Mission :**
Votre rôle est celui d'un **Spécialiste des Requêtes HTTP**. Votre mission est de corriger la méthode `search_item` en modifiant la manière dont les paramètres de recherche (`criteria`) sont construits, pour assurer une compatibilité maximale avec l'API GLPI.

**Contexte :**
Le projet est basé sur le livrable de la Mission 2.7. Le script de test a prouvé que la recherche via `search_item` échoue, même pour des objets dont l'existence est confirmée par la commande `list`.

**Objectif Principal :**
Modifier la construction du dictionnaire `params` dans la méthode `search_item` de `src/api_client.py` pour qu'elle corresponde à un format que la librairie `requests` et le serveur GLPI interpréteront sans ambiguïté.

---

#### **Base de Connaissances et Directives Permanentes :**

*   **Encodage des `params` :** La librairie `requests` transforme un dictionnaire de `params` en chaîne de requête URL. Pour des clés complexes comme `criteria[0][field]`, la syntaxe du dictionnaire Python doit être précise.
*   **Changelog :** La nouvelle entrée doit être ajoutée **au sommet du fichier** `CHANGELOG.md`.

---

#### **Tâches Détaillées :**

1.  **Mettre à jour la méthode `search_item` dans `src/api_client.py`** :
    *   Localisez la méthode `search_item(self, itemtype, item_name)`.
    *   **Remplacez la définition actuelle du dictionnaire `params`** par la version suivante, qui est plus explicite et moins sujette à des interprétations erronées par la librairie `requests` :
        ```python
        # Remplacer l'ancienne définition des params par celle-ci :
        params = [
            ('criteria[0][field]', 'name'),
            ('criteria[0][searchtype]', 'contains'),
            ('criteria[0][value]', item_name),
            ('forcedisplay[0]', '2') # '2' est l'ID du champ "ID" de l'objet
        ]
        ```
        *   **Pourquoi ce format ?** Passer les `params` sous forme d'une **liste de tuples** au lieu d'un dictionnaire garantit l'ordre des paramètres et évite tout problème d'encodage de clés complexes. C'est une technique de débogage robuste pour les requêtes HTTP.
        *   Nous ajoutons aussi `forcedisplay[0]=2` pour forcer GLPI à nous retourner l'ID de l'objet, ce qui rendra la réponse plus prévisible.

    *   **Ajustez l'analyse de la réponse** pour qu'elle soit cohérente avec `forcedisplay` :
        ```python
        # La logique d'analyse du JSON doit être :
        result = response.json()

        # Avec forcedisplay, la structure est prévisible.
        if result and isinstance(result.get('data'), list) and result['data']:
            first_item_data = result['data'][0]
            # La clé correspond à l'ID du champ que nous avons forcé à l'affichage, soit '2'.
            item_id = first_item_data.get('2') 
            if item_id:
                return item_id
        
        return None # Si on arrive ici, rien n'a été trouvé
        ```

2.  **Mettre à jour le script de test `test_api.py`** (optionnel mais recommandé) :
    *   Vous pouvez ajouter un test supplémentaire dans `test_api.py` pour rechercher un `NetworkEquipment` par son nom (ex: "SW reseaux") pour confirmer que la correction fonctionne pour plusieurs `itemtypes`.

---

#### **Livrable Final :**

1.  **Mise à jour du `CHANGELOG.md` :**
    *   Manus, vous devez documenter cette correction cruciale de la méthode de recherche en ajoutant une nouvelle entrée en haut du fichier.

2.  **Archive du Projet :**
    *   Créez une archive `.tar.gz` de l'intégralité du répertoire `glpi-explorer/` mis à jour.
    *   Nommez l'archive : **`mission_2.8_deliverable.tar.gz`**.

---
*Fin du Prompt de Mission*
