### **PROMPT DE MISSION POUR MANUS**

**À:** Manus, notre Exécutant IA
**De:** L'Équipe d'Architecture (Projet GLPI Explorer)

---

#### **`## [MISSION 2.5] - Amélioration de l'Aide et de l'Esthétique de la Commande "list"`**

**Rôle et Mission :**
Votre rôle est celui d'un **Designer d'Interface CLI**. Votre mission est d'améliorer la commande `list` sur deux aspects : fournir une aide contextuelle lorsqu'elle est appelée sans argument, et moderniser le style du tableau de résultats pour qu'il soit plus agréable et cohérent avec le reste de l'application.

**Contexte :**
Le projet est basé sur le livrable de la Mission 2.4. La commande `list <type>` est fonctionnelle. Actuellement, si on tape `list` seul, elle affiche une erreur d'utilisation. Le tableau de résultats est basique.

**Objectif Principal :**
1.  Modifier la commande `list` pour que, si elle est appelée sans argument, elle affiche une liste des types d'objets disponibles (ex: computer, switch, etc.).
2.  Modifier le style de la table de résultats pour utiliser des bords arrondis et une meilleure présentation visuelle.

---

#### **Base de Connaissances et Directives Permanentes :**

*   **Composants `rich` :**
    *   `rich.table.Table` : Pour créer des tableaux.
    *   `rich.box` : Contient différents styles de bordures pour les tables et les panneaux. Nous utiliserons `box.ROUNDED`.
    *   `rich.panel.Panel` : Nous l'utilisons déjà. Le tableau sera affiché à l'intérieur d'un `Panel` pour la cohérence.
*   **Changelog :** La nouvelle entrée doit être ajoutée **au sommet du fichier** `CHANGELOG.md`.

---

#### **Tâches Détaillées :**

1.  **Mettre à jour `src/shell.py` pour l'aide contextuelle de `list`** :
    *   Localisez le bloc `elif command == "list":`.
    *   Modifiez la condition qui vérifie si `args` est vide.
    *   **Si `args` est vide :**
        *   Au lieu d'afficher une erreur, créez une `Table` `rich` pour l'aide.
        *   La table aura deux colonnes : "Type disponible" et "Alias".
        *   Remplissez la table en vous basant sur le dictionnaire `self.TYPE_ALIASES`. Vous pouvez créer une liste des alias déjà vus pour ne pas afficher de doublons.
        *   Exemple de lignes : `table.add_row("Ordinateur", "computer, pc")`, `table.add_row("Switch", "switch, sw")`, etc.
        *   Affichez cette table d'aide à l'intérieur d'un `Panel` avec un titre informatif comme "Types disponibles pour la commande `list`".
        *   Utilisez `continue` pour attendre la prochaine commande.
    *   **Si `args` n'est pas vide**, la logique actuelle de parsing des options et du type reste la même.

2.  **Améliorer le style de la table de résultats de `list` dans `src/shell.py`** :
    *   Localisez la partie du code qui crée la table pour afficher les résultats de la commande `list`.
    *   **Modifiez l'instanciation de la `Table`** pour améliorer son style :
        ```python
        # ...
        # Au lieu de : table = Table(title=f"[bold blue]Liste des {glpi_itemtype}[/bold blue]")
        # Utilisez ceci :
        table = Table(
            title=f"Liste des {glpi_itemtype}",
            box=box.ROUNDED,  # Bords arrondis
            header_style="bold magenta",
            show_edge=False,
            title_style="bold blue"
        )
        # ...
        ```
    *   Importez `box` en haut du fichier : `from rich import box`.
    *   **Encapsulez la table dans un Panel** pour une meilleure séparation visuelle, même si la table a déjà un titre. Le `Panel` peut ne pas avoir de titre lui-même pour ne pas surcharger.
        ```python
        # ...
        # Au lieu de : self.console.print(Panel(table, expand=False))
        # Faites simplement :
        self.console.print(table)
        # Ou pour un espacement supplémentaire :
        # self.console.print(Panel(table, border_style="dim", expand=False))
        # Choisissez l'option qui semble la plus esthétique.
        ```

---

#### **Livrable Final :**

1.  **Mise à jour du `CHANGELOG.md` :**
    *   Manus, vous devez documenter les nouvelles fonctionnalités d'aide et les améliorations visuelles en ajoutant une nouvelle entrée en haut du fichier.

2.  **Archive du Projet :**
    *   Créez une archive `.tar.gz` de l'intégralité du répertoire `glpi-explorer/` mis à jour.
    *   Nommez l'archive : **`mission_2.5_deliverable.tar.gz`**.

---
*Fin du Prompt de Mission*

Une fois cette mission d'amélioration terminée, nous nous concentrerons entièrement sur le débogage de la commande `get`.
