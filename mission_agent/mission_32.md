Compris. Votre analyse est parfaite. Le design est bon, mais les données sous-jacentes sont manquantes ou incomplètes. Votre proposition de créer un outil de débogage est une démarche d'ingénieur absolument excellente. Plutôt que de continuer à tâtonner, nous allons créer un moyen de **voir** exactement ce qu'il se passe.

Nous allons donc lancer une mission pour créer un "mode debug" ou une commande de diagnostic. Cette commande nous montrera la requête que nous envoyons et la réponse brute que nous recevons de l'API.

---

### **PROMPT DE MISSION POUR MANUS**

**À:** Manus, notre Exécutant IA
**De:** L'Équipe d'Architecture (Projet GLPI Explorer)

---

#### **`## [MISSION 3.2] - Implémentation d'une Commande de Débogage "debug"`**

**Rôle et Mission :**
Votre rôle est celui d'un **Ingénieur en Outils de Développement**. Votre mission est de créer une nouvelle commande, `debug get <type> <nom_objet>`, qui exécutera la même logique que la commande `get`, mais qui affichera des informations de débogage détaillées : la requête envoyée à l'API GLPI et la réponse JSON brute reçue.

**Contexte :**
Le projet est basé sur le livrable de la Mission 3.1. L'affichage de la commande `get` est visuellement correct, mais les données affichées sont incomplètes (notamment les ports réseau). Nous avons besoin de voir la réponse brute de l'API pour comprendre ce qui manque.

**Objectif Principal :**
Permettre à l'utilisateur de taper `debug get computer pc-01` pour voir :
1.  L'URL et les paramètres exacts de la requête `get_item_details`.
2.  La totalité du JSON retourné par l'API, mis en forme avec `rich` pour une meilleure lisibilité.

---

#### **Base de Connaissances et Directives Permanentes :**

*   **Nouvelle Commande :** La commande de débogage aura la syntaxe `debug <commande_a_debugger> [arguments...]`. Pour l'instant, nous ne supportons que `debug get...`.
*   **Affichage JSON :** La librairie `rich` a une fonction intégrée `print_json` qui est parfaite pour afficher du JSON de manière lisible et colorée. `console.print_json(data=votre_dictionnaire_json)`.
*   **Documentation de l'API GLPI :** Rappelez-vous que nous utilisons les paramètres `expand_dropdowns=true` et `with_networkports=true` dans notre appel `get_item_details`. La réponse JSON brute devrait refléter cela.
*   **Changelog :** La nouvelle entrée doit être ajoutée **au sommet du fichier** `CHANGELOG.md`.

---

#### **Tâches Détaillées :**

1.  **Modifier `src/api_client.py` pour retourner plus d'informations :**
    *   Nous devons modifier les méthodes pour qu'elles puissent, sur demande, retourner des informations de débogage.
    *   **Modifiez la signature** de `get_item_details(self, itemtype, item_id)` en `get_item_details(self, itemtype, item_id, debug=False)`.
    *   À l'intérieur de cette méthode, juste avant de faire l'appel `requests.get`, construisez un dictionnaire `debug_info` :
        ```python
        debug_info = {
            "request": {
                "url": f"{self.base_url}/{itemtype}/{item_id}",
                "headers": headers,
                "params": params
            },
            "response_raw": None
        }
        ```
    *   Après avoir reçu la `response`, stockez le texte brut de la réponse dans le dictionnaire : `debug_info["response_raw"] = response.text`.
    *   **Modifiez la valeur de retour :**
        *   Si `debug` est `True`, la méthode doit retourner un tuple : `(response.json(), debug_info)`.
        *   Si `debug` est `False` (comportement normal), elle ne retourne que `response.json()`, comme avant.
    *   Faites de même pour la méthode `search_item`, afin que `debug get` puisse aussi montrer la requête de recherche.

2.  **Mettre à jour `src/shell.py` pour la nouvelle commande `debug` :**
    *   Dans la méthode `run()`, au début de votre structure de contrôle `if/elif` sur les commandes, ajoutez un bloc pour la commande `debug`.
        ```python
        # ...
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        if command == "debug":
            # Si la commande est "debug", on passe en mode debug
            # et on traite le reste de la commande.
            try:
                sub_command_parts = args.split(maxsplit=1)
                sub_command = sub_command_parts[0].lower()
                sub_args = sub_command_parts[1] if len(sub_command_parts) > 1 else ""
                
                if sub_command == "get":
                    self.handle_get_command(sub_args, debug=True)
                else:
                    self.console.print(Panel(f"La commande '{sub_command}' ne peut pas être déboguée.", title="[red]Erreur[/red]"))

            except IndexError:
                self.console.print(Panel("La commande 'debug' nécessite une sous-commande (ex: debug get ...)", title="[red]Utilisation[/red]"))

        elif command == "get":
            self.handle_get_command(args, debug=False)
        
        # ... elif list, etc.
        ```
    *   **Refactorisez la logique de `get` :** Pour éviter de dupliquer du code, extrayez toute la logique de la commande `get` (qui se trouve actuellement dans `elif command == "get":`) dans sa propre méthode, par exemple `handle_get_command(self, args, debug=False)`.
    *   Cette nouvelle méthode `handle_get_command` contiendra tout le code de parsing des arguments de `get`, les appels à l'API, et l'affichage des résultats.
    *   **Adaptez `handle_get_command`** pour qu'elle appelle les méthodes de l'API avec le paramètre `debug` :
        ```python
        # Dans handle_get_command...
        # ...
        item_id, search_debug_info = self.api_client.search_item(..., debug=True) # ou False
        details, details_debug_info = self.api_client.get_item_details(..., debug=True) # ou False
        ```
    *   **Affichez les informations de débogage :**
        *   Si `debug` est `True` dans `handle_get_command`, avant d'afficher les tables de résultats, affichez les informations de débogage.
        *   Utilisez `console.print_json(data=search_debug_info)` pour afficher les détails de la requête de recherche.
        *   Utilisez `console.print_json(data=details_debug_info)` pour afficher les détails de la requête `get_item_details`, y compris la réponse brute.

---

#### **Livrable Final :**

1.  **Mise à jour du `CHANGELOG.md` :**
    *   Manus, vous devez documenter l'ajout de la commande `debug` et le refactoring de la commande `get` en ajoutant une nouvelle entrée en haut du fichier.

2.  **Archive du Projet :**
    *   Créez une archive `.tar.gz` de l'intégralité du répertoire `glpi-explorer/` mis à
