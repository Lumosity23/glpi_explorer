### **PROMPT DE MISSION POUR MANUS**

**À:** Manus, notre Exécutant IA
**De:** L'Équipe d'Architecture (Projet GLPI Explorer)

---

#### **`## [MISSION 4.8] - Remplacement Forcé du Fichier `base_command.py`**

**Rôle et Mission :**
Votre rôle est celui d'un **Opérateur Système**. Vous n'allez pas réfléchir, vous allez exécuter une opération de remplacement de fichier précise et directe pour corriger une erreur d'importation persistante qui paralyse le projet.

**Contexte :**
Le projet est basé sur le livrable de la Mission 4.7. Ce livrable est défectueux. L'erreur `ModuleNotFoundError: No module named 'src.api'` persiste car le fichier `src/commands/base_command.py` n'a pas été corrigé.

**Objectif Principal :**
Remplacer le contenu entier de `src/commands/base_command.py` par le code correct fourni ci-dessous.

---

#### **Base de Connaissances et Directives Permanentes :**

*   **Opération de Remplacement :** Ne tentez pas de modifier le fichier. Effacez son contenu et collez le nouveau contenu.
*   **Changelog :** La nouvelle entrée doit être ajoutée **au sommet du fichier** `CHANGELOG.md`.

---

#### **Tâches Détaillées :**

1.  **Remplacer le contenu de `src/commands/base_command.py` :**
    *   Ouvrez le fichier `src/commands/base_command.py`.
    *   Supprimez **TOUT** son contenu actuel.
    *   Copiez-collez le code suivant, et **uniquement** ce code, dans le fichier :
        ```python
        # src/commands/base_command.py

        # Ces imports ne sont plus nécessaires ici car ils sont gérés
        # par les classes de commande individuelles ou passés via __init__.
        # from src.api_client import ApiClient
        # from src.config_manager import ConfigManager

        class BaseCommand:
            def __init__(self, api_client, console):
                """
                Initialise la commande de base.
                
                Args:
                    api_client: Une instance du client API déjà connecté.
                    console: Une instance de la console Rich pour l'affichage.
                """
                self.api_client = api_client
                self.console = console
                self.TYPE_ALIASES = {
                    'computer': 'Computer', 'pc': 'Computer',
                    'monitor': 'Monitor', 'screen': 'Monitor',
                    'networkequipment': 'NetworkEquipment', 'network': 'NetworkEquipment',
                    'switch': 'NetworkEquipment', 'sw': 'NetworkEquipment',
                    'hub': 'NetworkEquipment', 'hb': 'NetworkEquipment',
                    'peripheral': 'Peripheral',
                    'phone': 'Phone',
                    'printer': 'Printer',
                    'software': 'Software',
                    'ticket': 'Ticket',
                    'user': 'User',
                    'patchpanel': 'PassiveDevice', 'patch': 'PassiveDevice', 'pp': 'PassiveDevice',
                    'walloutlet': 'PassiveDevice', 'wo': 'PassiveDevice',
                    'cable': 'Cable', 'cb': 'Cable',
                }

            def execute(self, args):
                """
                La méthode principale que chaque sous-classe de commande doit implémenter.
                
                Args:
                    args (str): La chaîne d'arguments qui suit le nom de la commande.
                """
                raise NotImplementedError("La méthode execute() doit être implémentée par la sous-classe.")

        ```
    *   **Note importante :** J'ai commenté les imports `ApiClient` et `ConfigManager` car, après analyse de l'architecture, ils ne sont effectivement pas nécessaires dans la classe de base. L'instance `api_client` est passée via `__init__`. Cela rend le code encore plus propre et élimine la source de l'erreur.

---

#### **Livrable Final :**

1.  **Mise à jour du `CHANGELOG.md` :**
    *   Manus, vous devez documenter cette opération de remplacement forcé.

2.  **Archive du Projet :**
    *   Créez une archive `.tar.gz` de l'intégralité du répertoire `glpi-explorer/` corrigé.
    *   Nommez l'archive : **`mission_4.8_deliverable.tar.gz`**.

---
*Fin du Prompt de Mission*

Cette approche est la plus directe possible. Il n'y a aucune ambiguïté. Si, après cela, l'erreur persiste, le problème serait d'une nature que je ne peux actuellement pas concevoir. Mais je suis confiant que cela résoudra définitivement ce bug d'importation.
