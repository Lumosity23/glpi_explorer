#### **`## [MISSION 2.3] - Correction de l'Analyse des Arguments pour la Commande "get"`**

**Rôle et Mission :**
Votre rôle est celui d'un **Débogueur Python**. Votre mission principale est de corriger la logique d'analyse (parsing) des arguments pour la commande `get`, qui échoue actuellement à séparer le type d'objet de son nom, rendant la commande inutilisable.

**Contexte :**
Le projet est basé sur la version du code fournie précédemment (`shell.py`, `api_client.py`, etc.). La commande `list` est fonctionnelle, prouvant que la connexion et l'authentification sont correctes. La commande `get` échoue systématiquement car elle n'interprète pas bien ses arguments.

**Objectif Principal :**
Modifier `src/shell.py` pour que, lors d'un appel `get computer PC1`, le code identifie correctement `"computer"` comme le type et `"PC1"` comme le nom, puis lance la recherche appropriée qui, cette fois, doit réussir.

---

#### **Base de Connaissances et Directives Permanentes :**

*   **Logique de Parsing :** La chaîne `args` (qui contient par ex. `"computer PC1"`) doit être découpée en deux parties : le type et le nom. Le nom peut lui-même contenir des espaces (ex: `get walloutlet "WO Salle Réunion"`). `split(maxsplit=1)` est l'outil idéal pour cela.
*   **Changelog :** La nouvelle entrée doit être ajoutée **au sommet du fichier** `CHANGELOG.md`.

---

#### **Tâches Détaillées :**

1.  **Corriger la logique de la commande `get` dans `src/shell.py`** :
    *   Ouvrez le fichier `src/shell.py`.
    *   Localisez le bloc de code qui commence par `elif command == "get":`.
    *   **Remplacez la logique de parsing des arguments** à l'intérieur de ce bloc. La méthode actuelle est défaillante. La nouvelle logique doit être la suivante :
        ```python
        elif command == "get":
            if not args:
                self.console.print(Panel("[bold red]Erreur:[/bold red] La commande 'get' nécessite deux arguments.\nUsage: get <type> <nom_objet>", title="[red]Utilisation[/red]"))
                continue
            
            # Tenter de séparer le type du nom. Le nom est tout ce qui suit le type.
            try:
                user_type_alias, item_name = args.split(maxsplit=1)
            except ValueError:
                # Cette erreur se produit si 'args' ne contient qu'un seul mot.
                self.console.print(Panel("[bold red]Erreur:[/bold red] Syntaxe incorrecte. Il manque soit le type, soit le nom de l'objet.\nUsage: get <type> <nom_objet>", title="[red]Utilisation[/red]"))
                continue

            glpi_itemtype = self.TYPE_ALIASES.get(user_type_alias.lower())
            
            if not glpi_itemtype:
                self.console.print(Panel(f"[bold red]Erreur:[/bold red] Le type '{user_type_alias}' est inconnu.", title="[red]Type Inconnu[/red]"))
                continue
            
            # Le reste de la logique (status, appel api, affichage) qui suit est probablement déjà correct,
            # mais il dépendait de la bonne définition des variables glpi_itemtype et item_name.
            # Assurez-vous qu'il utilise bien ces variables.
            with self.console.status(f"Recherche de '{item_name}' ({glpi_itemtype})..."):
                # La méthode dans api_client.py a été renommée en search_item, assurons-nous d'utiliser le bon nom.
                item_id = self.api_client.search_item(glpi_itemtype, item_name)

            if item_id is None:
                self.console.print(Panel(f"[bold red]Erreur:[/bold red] Aucun élément de type '{user_type_alias}' nommé '{item_name}' trouvé.", title="[red]Non trouvé[/red]"))
            else:
                with self.console.status(f"[bold green]Récupération des détails de {item_name}...[/bold green]"):
                    details = self.api_client.get_item_details(glpi_itemtype, item_id)
                
                # Le reste du code d'affichage de la table est bon.
                if details:
                    # ... code d'affichage ...
                else:
                    # ... code d'erreur ...
        ```
    *   Cette nouvelle logique est robuste. Elle gère les cas où il manque des arguments et sépare correctement le type du nom, même si le nom contient des espaces.

2.  **Vérifier la cohérence dans `src/api_client.py` :**
    *   Assurez-vous que la méthode de recherche s'appelle bien `search_item(self, itemtype, item_name)`. Le code `shell.py` que vous m'avez fourni semble déjà l'appeler ainsi, mais une vérification est nécessaire pour éviter les `AttributeError`.

---

#### **Livrable Final :**

1.  **Mise à jour du `CHANGELOG.md` :**
    *   Manus, vous devez documenter cette correction en ajoutant une nouvelle entrée en haut du fichier.

2.  **Archive du Projet :**
    *   Créez une archive `.tar.gz` de l'intégralité du répertoire `glpi-explorer/` corrigé.
    *   Nommez l'archive : **`mission_2.3_deliverable.tar.gz`**.

---
*Fin du Prompt de Mission*
