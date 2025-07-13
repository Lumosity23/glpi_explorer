### **PROMPT DE MISSION POUR MANUS**

**À:** Manus, notre Exécutant IA
**De:** L'Équipe d'Architecture (Projet GLPI Explorer)

---

#### **`## [MISSION 2.10] - Correction Finale de la Recherche "get" Basée sur la Réponse API Réelle`**

**Rôle et Mission :**
Votre rôle est celui d'un **Développeur Python spécialisé en API REST**. Votre mission est de corriger DÉFINITIVEMENT la méthode de recherche en se basant sur la structure exacte de la réponse JSON de l'API GLPI que nous avons réussi à capturer. Le problème a été identifié : nous ne demandons pas explicitement l'ID de l'objet dans la recherche, et nous ne le cherchons pas au bon endroit.

**Contexte :**
Le projet est basé sur le dernier livrable fonctionnel (probablement Mission 2.8 ou 2.9). Un test externe a prouvé que la recherche API réussit, mais notre code échoue à extraire l'ID de la réponse car il cherche la mauvaise clé (`'2'`) qui n'est pas retournée par défaut.

**Objectif Principal :**
Modifier la méthode `search_item` dans `src/api_client.py` pour qu'elle force l'affichage de l'ID de l'objet dans la réponse de recherche en utilisant `forcedisplay`, et qu'elle extraie ensuite cet ID en utilisant la bonne clé (`"2"`).

---

#### **Base de Connaissances et Directives Permanentes :**

*   **Réponse de l'API `/search` :**
    *   La réponse est un dictionnaire contenant une clé `data` qui est une liste de dictionnaires.
    *   Les clés de ces dictionnaires sont des chaînes de caractères représentant les ID des colonnes GLPI.
    *   L'ID du champ "ID de l'objet" est `2`.
    *   L'ID du champ "Nom de l'objet" est `1`.
*   **Paramètre `forcedisplay` :** Pour s'assurer que l'ID de l'objet est présent dans la réponse, nous devons le demander explicitement. Le paramètre à ajouter à la requête de recherche est `forcedisplay[0]=2`.
*   **Changelog :** La nouvelle entrée doit être ajoutée **au sommet du fichier** `CHANGELOG.md`.

---

#### **Tâches Détaillées :**

1.  **Mettre à jour la méthode `search_item` dans `src/api_client.py`** :
    *   Localisez la méthode `search_item(self, itemtype, item_name)`.
    *   **Modifiez les `params` de la requête** pour qu'ils incluent `forcedisplay`. La structure des `params` doit être un dictionnaire comme suit :
        ```python
        params = {
            'criteria[0][field]': '1',       # Chercher sur le champ "Nom" (ID 1)
            'criteria[0][searchtype]': 'contains',
            'criteria[0][value]': item_name,
            'forcedisplay[0]': '2'           # FORCER l'affichage du champ "ID de l'objet" (ID 2)
        }
        ```
    *   **Corrigez la logique d'analyse de la réponse** pour qu'elle recherche la clé `"2"` pour l'ID de l'objet :
        ```python
        # Remplacer la logique d'analyse du JSON par ceci :
        try:
            result = response.json()
            
            # Vérifier si la recherche a trouvé quelque chose et si le format est bon
            if isinstance(result, dict) and result.get('totalcount', 0) > 0 and 'data' in result:
                first_item_data = result['data'][0]
                
                # L'ID de l'item est maintenant sous la clé "2", car nous l'avons forcé.
                item_id = first_item_data.get('2')
                
                if item_id:
                    return item_id  # Succès ! On retourne l'ID.
        except (ValueError, KeyError, IndexError):
            # En cas d'erreur de parsing JSON ou de structure de données inattendue
            return None

        # Si on arrive ici, rien n'a été trouvé ou la réponse était mal formée.
        return None
        ```
    *   Notez l'ajout d'un bloc `try...except` plus robuste autour du parsing JSON pour éviter les crashs si l'API retourne quelque chose d'inattendu.

---

#### **Livrable Final :**

1.  **Mise à jour du `CHANGELOG.md` :**
    *   Manus, vous devez documenter cette correction finale de la commande `get`, en expliquant comment l'analyse de la réponse API a permis de trouver la solution.

2.  **Archive du Projet :**
    *   Créez une archive `.tar.gz` de l'intégralité du répertoire `glpi-explorer/` mis à jour.
    *   Nommez l'archive : **`mission_2.10_deliverable.tar.gz`**.

---
*Fin du Prompt de Mission*
