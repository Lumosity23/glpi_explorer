D'accord. C'est le moment de sortir l'artillerie lourde. Nous avons épuisé toutes les hypothèses raisonnables sur la structure de la requête. Le fait que `list` fonctionne mais pas `search` sur le même `itemtype` est un paradoxe qui ne peut s'expliquer que par une subtilité de l'API que nous ne voyons pas.

Il n'y a qu'une seule façon de savoir ce qui se passe **exactement** : nous devons intercepter et inspecter la requête HTTP brute qui est envoyée par l'ancien projet (celui qui fonctionnait) et la comparer à celle envoyée par le nôtre.

Pour cela, nous avons besoin d'un "proxy de débogage". C'est un outil qui se place entre notre application et le serveur GLPI pour enregistrer tout le trafic. Cependant, c'est complexe à mettre en place.

Il y a une méthode plus simple et intégrée au code : **demander à la librairie `requests` de nous dire ce qu'elle s'apprête à envoyer.**

Nous allons modifier notre script de test pour qu'il n'envoie pas la requête, mais qu'il nous montre l'URL complète qu'il a construite. C'est la source de vérité ultime.

---

### **PROMPT DE MISSION POUR MANUS**

**À:** Manus, notre Exécutant IA
**De:** L'Équipe d'Architecture (Projet GLPI Explorer)

---

#### **`## [MISSION 2.9] - Débogage Ultime de la Requête de Recherche via Inspection d'URL`**

**Rôle et Mission :**
Votre rôle est celui d'un **Expert en Débogage Réseau**. Votre mission n'est pas de faire fonctionner la recherche, mais de modifier le code pour qu'il nous révèle l'URL exacte qu'il essaie d'appeler. Cela nous permettra de la comparer à ce que l'API attend.

**Contexte :**
Le projet est basé sur le livrable de la Mission 2.8. Toutes les tentatives pour corriger la recherche ont échoué. Nous passons en mode "inspection de bas niveau".

**Objectif Principal :**
Modifier la méthode `search_item` dans `src/api_client.py` pour qu'elle n'exécute pas la requête, mais qu'elle construise l'objet `Request` et imprime son URL préparée (`prepared_request.url`). Cela nous montrera l'URL finale avec tous les paramètres encodés.

---

#### **Base de Connaissances et Directives Permanentes :**

*   **Librairie `requests` - Requêtes Préparées :** La librairie permet de préparer une requête sans l'envoyer. On crée un objet `requests.Request`, puis un objet `PreparedRequest` via `session.prepare_request()`. Cet objet `PreparedRequest` possède un attribut `.url` qui contient l'URL finale, prête à être envoyée.
*   **Changelog :** La nouvelle entrée doit être ajoutée **au sommet du fichier** `CHANGELOG.md`.

---

#### **Tâches Détaillées :**

1.  **Mettre à jour la méthode `search_item` dans `src/api_client.py`** :
    *   Localisez la méthode `search_item(self, itemtype, item_name)`.
    *   **Commentez ou supprimez toute la logique existante** à l'intérieur de la méthode.
    *   **Remplacez-la par le code d'inspection suivant :**
        ```python
        def search_item(self, itemtype, item_name):
            if not self.session_token:
                print("DEBUG: Pas de session token, recherche annulée.")
                return None

            # Préparer la requête sans l'envoyer
            url = f"{self.base_url}/search/{itemtype}"
            params = [
                ('criteria[0][field]', 'name'),
                ('criteria[0][searchtype]', 'contains'),
                ('criteria[0][value]', item_name),
                ('forcedisplay[0]', '2')
            ]
            headers = {
                "Session-Token": self.session_token,
                "App-Token": self.app_token,
            }

            # Utiliser la mécanique de "Prepared Request" de la librairie requests
            session = requests.Session()
            request = requests.Request('GET', url, headers=headers, params=params)
            prepared_request = session.prepare_request(request)
            
            # IMPRIMER L'URL EXACTE QUI AURAIT ÉTÉ APPELÉE
            print("\n--- DEBUG URL DE RECHERCHE ---")
            print(f"URL CONSTRUITE: {prepared_request.url}")
            print("----------------------------\n")

            # Pour cette mission de débogage, nous n'exécutons pas la requête.
            # Nous retournons None pour que le script de test signale un échec, 
            # mais nous aurons l'URL dans la console.
            return None
        ```
    *   Cette modification transformera temporairement `search_item` en un outil de diagnostic.

2.  **Laisser le reste du code inchangé.** Le script `test_api.py` appellera cette méthode modifiée, et au lieu d'une erreur réseau, nous verrons l'URL s'imprimer dans la console.

---

#### **Livrable Final :**

1.  **Mise à jour du `CHANGELOG.md` :**
    *   Manus, vous devez documenter cette mission de débogage, en expliquant que la méthode `search_item` a été temporairement modifiée pour inspecter l'URL générée.

2.  **Archive du Projet :**
    *   Créez une archive `.tar.gz` de l'intégralité du répertoire `glpi-explorer/` mis à jour.
    *   Nommez l'archive : **`mission_2.9_deliverable.tar.gz`**.

---
*Fin du Prompt de Mission*

Une fois que Manus aura produit ce code, exécutez le script `test_api.py`. Vous n'aurez plus d'erreur réseau, mais vous verrez une nouvelle section de débogage dans la console avec l'URL exacte. **Copiez-collez-moi l'intégralité de cette URL.** C'est la pièce à conviction qui nous manque.
