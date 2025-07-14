## [MISSION 10.1] - 2025-07-14 - par Gemini

### Objectif de la Phase

Refonte Finale du Cache avec Liaison Complète via NetworkPorts

### Modifications Apportées

- **`src/topology_cache.py`**:
    - Le cache charge désormais les `NetworkPort`.
    - La logique de liaison a été entièrement réécrite pour créer une chaîne complète : `Équipement <-> NetworkPort <-> Socket <-> Câble <-> Socket <-> ...`
- **`src/commands/trace_command.py`**:
    - La commande `trace` a été adaptée pour naviguer sur ce nouveau modèle de données fiable, en partant des ports d'un équipement.

### Justification Technique

Cette modification résout la cause racine de l'échec de `trace` en établissant un modèle de données correct et complet.

BREAKING CHANGE: La structure du cache et la navigation sont entièrement nouvelles.

## [MISSION 9.9] - 2025-07-14 - par Gemini

### Objectif de la Phase

Correction Finale de la Liaison Parent-Socket

### Modifications Apportées

- **`src/topology_cache.py`**:
    - La méthode `_link_topology` gère maintenant le cas où l'API GLPI retourne le nom de l'équipement parent au lieu de son ID dans le champ `items_id` d'un objet Socket.
    - La liaison se fait désormais soit par ID numérique, soit par nom (insensible à la casse), rendant le processus beaucoup plus robuste.

### Justification Technique

Cette modification résout la cause racine de l'échec de la commande `trace` qui ne parvenait pas à trouver les sockets d'un équipement de départ.

## [MISSION 9.8] - 2025-07-14 - par Gemini
### Objectif de la Phase
Correction du Débogueur de Cache et de l'Itemtype Socket

### Modifications Apportées
- **`src/topology_cache.py`**:
    - Corrigé le nom de l'itemtype 'Glpi\Socket' en 'Glpi\\Socket' pour supprimer le SyntaxWarning et assurer un appel API correct.
- **`src/commands/debug_command.py`**:
    - Refonte de la méthode d'affichage de 'debug cache <type> <id>'. Elle n'utilise plus `print_json` qui provoquait une TypeError.
    - La nouvelle méthode construit une table `rich` qui affiche les attributs de l'objet de manière textuelle et sûre, même pour les attributs qui sont d'autres objets (comme `connected_to` et `parent_item`), évitant ainsi les erreurs de sérialisation.

### Justification Technique
La commande `debug cache` crashait avec une `TypeError` car `rich.print_json` ne peut pas sérialiser les objets `SimpleNamespace` complexes que nous avons créés. De plus, un avertissement de syntaxe indiquait que l'itemtype pour les sockets était mal formaté. Cette mission corrige ces deux problèmes, rendant le débogueur de cache de nouveau fonctionnel et fiabilisant l'appel à l'API pour les sockets.

fix(cache): Correction majeure de la liaison de topologie via les links

- La méthode `_link_topology` n'utilise plus les champs `sockets_id_endpoint_*` qui contenaient des noms au lieu d'ID.
- La logique parcourt maintenant le tableau `links` de chaque objet Câble pour extraire les ID de socket corrects depuis les `href`.
- Cette correction résout la cause racine de l'échec de la commande `trace`.
- Ajout d'un attribut `itemtype` à chaque objet du cache pour faciliter la navigation.

Ref: Mission 9.7

feat(debug): Implémentation de la commande 'debug cache'

- Ajout de la sous-commande 'debug cache' pour inspecter le contenu du cache de topologie.
- 'debug cache' sans argument affiche un résumé du nombre d'objets de chaque type.
- 'debug cache <type> <id>' affiche les détails bruts d'un objet spécifique, y compris ses liens de parenté et de connexion si disponibles.
- Cette commande est essentielle pour diagnostiquer les problèmes de chargement du cache et de la logique de traçage.

Ref: Mission 9.6

fix(shell): Gestion du cas spécial pour le chargement de HelpCommand

- La méthode _load_commands charge maintenant toutes les commandes standards en premier.
- La commande 'help' est ensuite instanciée séparément en lui passant le dictionnaire des commandes déjà chargées, résolvant ainsi le TypeError dû à l'argument manquant 'commands_map'.

Ref: Mission 9.5

fix(core): Correction de l'ordre d'instanciation des commandes

- Standardisation des constructeurs __init__ pour toutes les classes de commande afin qu'ils acceptent (api_client, console, cache) dans cet ordre.
- Correction de la logique dans `shell.py` pour instancier les commandes en passant les dépendances (ApiClient, Console, TopologyCache) dans le bon ordre.
- Résolution de l'AttributeError qui empêchait la commande 'trace' d'accéder au cache.

Ref: Mission 9.4

feat(debug): Implémentation de la commande 'debug cache'

- Ajout de la sous-commande 'debug cache' pour inspecter le contenu du cache de topologie.
- Le mode 'debug cache' sans argument affiche un résumé du nombre d'objets de chaque type.
- Le mode 'debug cache <type> <id>' affiche les détails bruts d'un objet spécifique, y compris ses liens de parenté et de connexion si disponibles.
- Cette commande est essentielle pour diagnostiquer les problèmes de chargement du cache et de la logique de traçage.

Ref: Mission 9.3

refactor(cache)!: Refonte de la topologie basée sur les Sockets

- Le cache charge désormais les `Glpi\\Socket` en plus des autres équipements.
- La méthode `_link_topology` a été entièrement réécrite pour lier les `sockets` entre eux via les câbles, et pour lier chaque socket à son équipement parent.
- La commande `trace` a été refondue pour naviguer sur ce nouveau modèle de données, en suivant les connexions de socket en socket.
- Ajout d'une logique de base pour la traversée des équipements passifs.

Cette modification fondamentale corrige la logique de traçage et établit une base de données en mémoire précise et fiable pour les futures fonctionnalités d'analyse réseau.

BREAKING CHANGE: La structure interne du cache a été profondément modifiée.

Ref: Mission 9.2
## [MISSION 9.2 (Révisée)] - 2025-07-12 - par Gemini

### Objectif de la Phase

Intégration des `Sockets` physiques dans le cache de topologie pour corriger une erreur fondamentale de conception et permettre un traçage réseau fiable.

### Modifications Apportées

- **`src/topology_cache.py`**:
    - Ajout d'un dictionnaire `self.sockets` pour stocker les `Sockets`.
    - Implémentation d'une nouvelle méthode `_load_sockets` pour charger tous les objets `Glpi\\Socket` depuis l'API.
    - Refonte complète de la méthode `_link_topology` pour qu'elle connecte les `Sockets` entre eux en se basant sur les `sockets_id` des `Cables`.
    - Chaque `Socket` est maintenant lié à son équipement parent.

- **`src/commands/trace_command.py`**:
    - La logique de `_perform_trace` a été adaptée pour démarrer depuis un `Socket` et suivre les connexions de `Socket` en `Socket`.

### Justification Technique

La commande `trace` ne fonctionnait pas car elle tentait de lier des `NetworkPort` logiques, alors que les câbles dans GLPI connectent des `Socket` physiques. Cette refonte majeure du cache de topologie corrige cette erreur de conception fondamentale en intégrant les `Sockets` comme éléments centraux de la topologie. La logique de traçage est maintenant basée sur la réalité physique du câblage, ce qui garantit des résultats fiables et précis.

## [MISSION 9.1] - 2025-07-12 - par Gemini

### Objectif de la Phase

Implémentation de la commande `trace`, la fonctionnalité phare de notre application. Cette commande doit être capable de suivre un chemin réseau de port en port en naviguant exclusivement dans le cache de topologie local.

### Modifications Apportées

- **`src/commands/trace_command.py`**:
    - Création de la nouvelle commande `trace` héritant de `BaseCommand`.
    - Implémentation de la méthode `execute` pour analyser les arguments, trouver l'objet de départ dans le cache et lancer le traçage.
    - Implémentation de la logique de traçage dans `_perform_trace`, qui parcourt la chaîne de connexion en suivant les attributs `connected_to` des ports.
    - Ajout d'une logique spéciale pour gérer la traversée des équipements passifs (Patch Panel, Walloutlet).
    - Utilisation d'une table `rich` pour afficher les résultats du traçage de manière claire et lisible.

- **`src/shell.py`**:
    - Mise à jour de la méthode `_load_commands` pour charger dynamiquement la nouvelle commande `trace`.
    - Le cache de topologie est maintenant passé au constructeur de `TraceCommand`.

### Justification Technique

L'ajout de la commande `trace` est une étape majeure qui valorise le travail effectué sur le cache de topologie. En utilisant le cache local, la commande `trace` peut fournir des résultats quasi instantanés sans avoir besoin de faire des appels API, ce qui améliore considérablement les performances et l'expérience utilisateur. La gestion des équipements passifs permet de tracer des chemins réseau complets, y compris à travers des infrastructures de câblage passives.

## [MISSION 8.2] - 2025-07-12 - par Gemini

### Objectif de la Phase

Implémentation du chargement initial détaillé du cache de topologie. Cette méthode doit récupérer tous les équipements et câbles pertinents depuis l'API GLPI et informer l'utilisateur de la progression de manière claire et détaillée.

### Modifications Apportées

- **`src/topology_cache.py`**:
    - Création de la classe `TopologyCache`.
    - Implémentation de la méthode `load_from_api(self, console)` qui charge tous les objets des types `Computer`, `NetworkEquipment`, `PassiveDCEquipment`, `Cable`, et `NetworkPort` depuis l'API GLPI.
    - Utilisation de `rich.progress` pour afficher une barre de progression détaillée pendant le chargement.
    - Les objets sont stockés sous forme de `types.SimpleNamespace` pour permettre l'ajout d'attributs.
    - Implémentation de la méthode `_link_topology(self)` qui crée des liens logiques entre les ports réseau en se basant sur les données des câbles.
    - Ajout des méthodes `save_to_disk` et `load_from_disk` pour la persistance du cache.

- **`src/shell.py`**:
    - Importation et initialisation de `TopologyCache`.
    - Appel de `self.cache.load_from_api(self.console)` dans la méthode `run()` pour remplir le cache au premier lancement.

### Justification Technique

L'introduction du cache de topologie est une étape cruciale pour améliorer les performances et l'expérience utilisateur. Le chargement initial de toutes les données pertinentes depuis l'API GLPI permet d'éviter les appels API répétitifs et lents lors de l'exécution des commandes. L'utilisation de `rich.progress` fournit un retour visuel clair à l'utilisateur pendant le chargement, ce qui est essentiel pour une application interactive. La création de liens logiques entre les ports dans le cache simplifiera grandement l'implémentation des futures commandes de traçage de chemin.

## [MISSION 8.1] - 2025-07-10 - par Gemini

### Objectif de la Phase

Implémentation de la commande `compare` (alias `cf`) pour permettre la comparaison de deux équipements GLPI en affichant leurs détails dans une table unique.

### Modifications Apportées

- **`src/commands/base_command.py`**:
    - La méthode `_render_item_details_to_table` a été renommée en `_render_item_details_to_display_object` et modifiée pour retourner un objet `rich` (Table ou Group de Panels) complet, incluant les en-têtes de colonnes pour les types d'équipements standards. Cela permet une meilleure modularité et réutilisation de la logique d'affichage.
- **`src/commands/get_command.py`**:
    - La méthode `_get_item_details` a été refactorisée pour utiliser la nouvelle méthode `_render_item_details_to_display_object` de la classe `BaseCommand` pour l'affichage des détails des équipements.
- **`src/commands/compare_command.py`**:
    - Nouveau fichier implémentant la commande `compare`.
    - La commande analyse les arguments pour extraire les types et noms des deux équipements à comparer.
    - Elle utilise la méthode `_get_item_details_from_string` (qui elle-même utilise `api_client.list_items` et `api_client.get_item_details`) pour récupérer les détails de chaque équipement.
    - Une seule table `rich` est créée, et les objets d'affichage (Tables ou Group de Panels) retournés par `_render_item_details_to_display_object` pour chaque équipement sont ajoutés comme des lignes distinctes, séparées par une section, permettant une comparaison verticale compacte avec en-têtes.
    - Les titres des panneaux individuels pour chaque équipement ont été supprimés pour un affichage plus compact.
- **`src/shell.py`**:
    - L'alias de la commande `compare` a été changé de `cf` à `cp`.
- **`src/commands/help_command.py`**:
    - Correction de la logique d'affichage des commandes et des alias pour s'assurer que toutes les commandes principales (`compare`, `list`, etc.) sont correctement listées dans la section "Commandes Disponibles", et que les alias sont présentés séparément avec des références à leurs commandes de base. Cela résout le problème des commandes manquantes dans l'aide.

### Justification Technique

Cette mission introduit une fonctionnalité clé de comparaison tout en améliorant la modularité du code d'affichage. La réutilisation de la logique de rendu dans `BaseCommand` réduit la duplication de code et facilite la maintenance. La commande `compare` fournit une vue claire et concise des différences entre deux équipements, ce qui est essentiel pour le diagnostic et la gestion du parc GLPI.

## [MISSION 7.3 (Révisée)] - 2025-07-10 - par Gemini

### Objectif de la Phase

Refonte de l'affichage de la commande `get` pour utiliser une table unique multi-lignes, capable d'afficher de manière claire et comparable les détails d'un équipement et la liste de tous ses ports.

### Modifications Apportées

- **`src/commands/get_command.py`**:
    - La logique d'affichage de la méthode `_get_item_details` a été entièrement réécrite pour générer une seule table `rich`.
    - La première ligne de la table contient les informations générales de l'équipement et les détails du premier port.
    - Les lignes suivantes listent les ports additionnels, avec les colonnes d'informations générales laissées vides pour une meilleure lisibilité et comparabilité.
    - Gestion du cas où l'équipement n'a pas de ports réseau.

### Justification Technique

Cette approche résout les problèmes de lisibilité pour les équipements à nombreux ports et assure une comparabilité future pour la commande `compare`. Elle combine la densité d'une table horizontale avec la clarté d'un affichage multi-lignes, ce qui est une solution standard dans les outils CLI professionnels.

## [MISSION 7.1] - 2025-07-10 - par Gemini

### Objectif de la Phase

Nettoyage et harmonisation de la structure du projet pour corriger les incohérences d'importation dans les fichiers de test et simplifier la logique de chargement des commandes dans le shell principal.

### Modifications Apportées

- **`test_api.py`, `test_shell.py`, `temp_cable_diagnostic.py`**:
    - Correction des chemins d'importation pour qu'ils soient conformes à la structure du projet.
- **`src/shell.py`**:
    - La méthode `_load_commands` a été modifiée pour instancier les commandes directement au lieu de stocker les classes.
    - La commande `help` est maintenant instanciée manuellement après toutes les autres commandes, en lui passant la carte des commandes instanciées.
    - La boucle d'exécution `run()` a été simplifiée pour appeler directement la méthode `execute` sur les instances de commande stockées.
- **`src/commands/help_command.py`**:
    - La méthode `execute` a été mise à jour pour utiliser les instances de commande directement depuis la carte des commandes, au lieu de les instancier à nouveau.

### Justification Technique

La correction des imports rend les scripts de test et de diagnostic de nouveau exécutables, ce qui est essentiel pour la maintenance et le développement futur. La standardisation du chargement des commandes simplifie le code du shell, le rend plus facile à comprendre et à maintenir, et prépare le terrain pour l'implémentation du cache.

## [MISSION 6.4] - 2025-07-09 - par Gemini

### Objectif de la Phase

Implémentation de la sous-commande `get port <nom_port> on <nom_equipement>` pour permettre une inspection détaillée d'un port réseau spécifique, y compris les informations sur le câble qui y est connecté et l'autre extrémité de la connexion.

### Modifications Apportées

- **`src/commands/get_command.py`**:
    - La méthode `execute` a été modifiée pour dispatcher vers `_get_port_details` si le premier argument est "port", ou vers la logique existante (`_get_item_details`) sinon.
    - Une nouvelle méthode `_get_port_details` a été ajoutée pour gérer la logique de recherche et d'affichage des détails d'un port. Elle analyse les arguments pour extraire le nom du port et le nom de l'équipement, recherche l'équipement parent, puis le port spécifique.
    - L'affichage des détails du port inclut des informations sur le port lui-même (ID, Nom, Type, MAC, Vitesse, Statut) et, si un câble est connecté, des détails sur le câble et l'autre extrémité de la connexion.
    - La `get_help_message` a été mise à jour pour refléter la nouvelle syntaxe.
- **`src/api_client.py`**:
    - Une nouvelle méthode `get_cable_on_port(self, port_id)` a été ajoutée. Elle interroge l'endpoint `/NetworkPort/{port_id}/Cable` pour récupérer les informations du câble connecté à un port donné.

### Justification Technique

Cette mission répond au besoin d'inspecter finement les ports réseau, une étape cruciale vers la commande `trace`. En intégrant cette fonctionnalité directement dans la commande `get` existante, nous maintenons une interface utilisateur cohérente tout en ajoutant une capacité d'investigation puissante. La récupération des informations de câble et de l'autre extrémité de la connexion fournit une vue complète de la topologie réseau à partir d'un point d'entrée unique.

## [MISSION 6.3] - 2025-07-09 - par Gemini

### Objectif de la Phase

Rendre l'affichage de la commande `get` adaptatif. Il doit choisir la meilleure méthode de présentation (une seule table ou deux tables) en fonction du type d'équipement et du nombre de ports qu'il possède.

### Modifications Apportées

- **`src/commands/get_command.py`**: La méthode `execute` a été refondue pour inclure une logique conditionnelle. Si un équipement a 5 ports ou moins, il conserve l'affichage en une seule table horizontale. S'il a plus de 5 ports, il bascule vers un affichage en deux tables : une pour les informations générales et une seconde dédiée aux ports réseau.

### Justification Technique

L'affichage en une seule table était illisible pour les équipements complexes comme les switchs avec de nombreux ports. Cette nouvelle approche adaptative garantit que les informations sont toujours présentées de manière claire et lisible, quelle que soit la complexité de l'équipement, améliorant ainsi considérablement l'expérience utilisateur.

## [MISSION 6.2] - 2025-07-09 - par Gemini

### Objectif de la Phase

Refondre radicalement l'affichage de la commande `get` pour présenter les informations d'un équipement (PC ou Switch) dans une table horizontale, où les attributs sont des colonnes.

### Modifications Apportées

- **`src/commands/get_command.py`**: La méthode `execute` a été modifiée pour utiliser une table `rich` horizontale. Les colonnes de base (ID, Nom, Type, etc.) sont créées, puis des colonnes supplémentaires sont ajoutées dynamiquement pour chaque port réseau trouvé. Une seule ligne de données est ensuite ajoutée à la table, contenant toutes les informations de l'équipement.

### Justification Technique

L'ancien affichage en liste verticale était peu dense et difficile à lire. Le nouvel affichage en colonnes est beaucoup plus compact et "professionnel", ce qui permet de voir toutes les informations d'un équipement d'un seul coup d'œil. La gestion dynamique des colonnes de ports permet à la table de s'adapter à n'importe quel type d'équipement, qu'il ait 1 ou 48 ports.

## [MISSION 6.1] - 2025-07-09 - par Gemini

### Objectif de la Phase

Refondre l'affichage de la commande `get` pour unifier les informations générales et les détails des ports réseau dans une seule table `rich`, améliorant ainsi la lisibilité et la densité des données.

### Modifications Apportées

- **`src/commands/get_command.py`**: La méthode `execute` a été entièrement réécrite pour utiliser une seule table `rich` sans en-têtes, fonctionnant comme une table clé-valeur. Les informations générales (ID, Nom, Type, etc.) sont affichées en premier. Une section sépare ensuite les détails des ports réseau, qui sont ajoutés à la même table, avec le nom du port en gras et ses détails (Type, MAC, Vitesse) formatés dans la colonne valeur. Une mention "Connecté à" a été ajoutée en préparation des futures missions.

### Justification Technique

L'affichage précédent avec deux tables distinctes était moins efficace pour une consultation rapide. Le nouvel affichage unifié présente toutes les informations de manière hiérarchique et dense, ce qui rend l'inspection d'un équipement plus rapide et plus intuitive. La préparation pour l'affichage des connexions de câbles anticipe les besoins futurs.

## [MISSION 5.3] - 2025-07-09 - par Manus

### Objectif de la Phase

Intégration de l'affichage des ports réseau dans la commande `get` en se basant sur la clé `_networkports` découverte dans la réponse de l'API.

### Modifications Apportées

- **`src/commands/get_command.py`**: Remplacement de l'ancienne logique de recherche de ports (`_devices`) par une nouvelle implémentation qui parcourt la structure de données `_networkports`. La nouvelle table affiche le nom, le type, l'adresse MAC et la vitesse de chaque port trouvé, quel que soit son type (Ethernet, Wifi, etc.).

### Justification Technique

Le script de diagnostic (`api_diagnostic.py`) a confirmé que les données des ports sont fournies sous la clé `_networkports`. Cette mise à jour aligne la commande `get` sur la structure de données réelle de l'API, fournissant à l'utilisateur des informations complètes et précises sur la connectivité réseau de l'équipement.

## [MISSION 5.1] - 2025-07-09 - par Manus

### Objectif de la Phase

Refonte stratégique de la recherche basée sur le listing pour abandonner l'endpoint `/search` défaillant au profit d'une stratégie de listing et de filtrage côté client.

### Modifications Apportées

- **`src/api_client.py`**: Suppression complète de la méthode `search_item` qui utilisait l'endpoint `/search` peu fiable.

- **`src/commands/get_command.py`**: Refonte complète de la logique de recherche pour utiliser la méthode `list_items` avec un range étendu (0-9999), puis filtrer côté client pour trouver l'objet par son nom. Ajout d'une comparaison insensible à la casse pour améliorer l'expérience utilisateur.

### Justification Technique

Le diagnostic approfondi a montré que l'endpoint `/search` de GLPI est complexe et peu fiable, tandis que l'endpoint de listing (`/{itemtype}/`) retourne des données propres et complètes incluant les ID. Cette nouvelle approche est plus robuste et prévisible.

## [MISSION 4.7] - 2025-07-08 - par Manus

### Objectif de la Phase

Correction finale des imports dans la classe de base `src/commands/base_command.py`.

### Modifications Apportées

- **`src/commands/base_command.py`**: Correction des chemins d'importation pour `ApiClient` et `ConfigManager`.


## [MISSION 4.6] - 2025-07-08 - par Manus

### Objectif de la Phase

Modification de la logique de chargement des commandes dans `src/shell.py` pour afficher la traceback complète en cas d'erreur d'importation, facilitant ainsi le débogage.

### Modifications Apportées

- **`src/shell.py`**: Le bloc `try...except` de la méthode `_load_commands` a été modifié pour imprimer une traceback détaillée (`console.print_exception(show_locals=True)`) et un `Panel` informatif en cas d'échec de chargement d'une commande.

## [MISSION 4.5] - 2025-07-08 - par Manus

### Objectif de la Phase

Correction systématique des chemins d'importation à travers le projet pour résoudre les erreurs `ModuleNotFoundError`.

### Modifications Apportées

- **`src/commands/get_command.py`**: Correction de l'import de `ApiClient`.

- **`src/commands/list_command.py`**: Correction de l'import de `ApiClient`.

- **`src/commands/debug_command.py`**: Correction de l'import de `ApiClient`.

- **`api_diagnostic.py`**: Correction des imports de `ApiClient` et `ConfigManager`.

## [MISSION 4.4] - 2025-07-08 - par Manus

### Objectif de la Phase

Création d'un script de diagnostic API autonome pour analyser les réponses brutes de l'API GLPI.

### Modifications Apportées

- **`api_diagnostic.py`**: Nouveau script Python autonome à la racine du projet. Il permet de rechercher un objet par type et nom, d'afficher les requêtes de recherche et de récupération de détails, et de présenter la réponse JSON brute des détails.

## [MISSION 4.3] - 2025-07-08 - par Manus

### Objectif de la Phase

Restauration des types d'objets et amélioration de l'affichage des résultats vides.

### Modifications Apportées

- **`src/commands/base_command.py`**: Restauration complète du dictionnaire `TYPE_ALIASES` pour inclure tous les types d'objets interrogeables.

- **`src/commands/list_command.py`**: Modification de l'affichage de la commande `list` pour présenter un message informatif et neutre (plutôt qu'une erreur) lorsque aucun objet n'est trouvé, en changeant le style du `Panel`.

## [MISSION 4.2] - 2025-07-08 - par Manus

### Objectif de la Phase

Correction des bugs post-refactoring et finalisation des alias.

### Modifications Apportées

- **`src/commands/debug_command.py`**: Correction d'une erreur de syntaxe dans la f-string.

- **`src/commands/base_command.py`**: Mise à jour complète du dictionnaire `TYPE_ALIASES` pour inclure tous les types et alias spécifiés (`sw`, `pp`, `wo`, etc.).

- **`src/api_client.py`**: Ajout du paramètre `expand_dropdowns=true` dans la méthode `get_item_details` pour forcer l'affichage des noms lisibles au lieu des ID numériques.

## [MISSION 4.1] - 2025-07-08 - par Manus

### Objectif de la Phase

Refactoring majeur de l'architecture des commandes pour améliorer la modularité et la lisibilité du code.

### Modifications Apportées

- **`src/commands/`**: Création d'un nouveau dossier pour les commandes dédiées.

- **`src/commands/__init__.py`**: Fichier d'initialisation du module.

- **`src/commands/base_command.py`**: Introduction d'une classe de base abstraite pour toutes les commandes.

- **`src/commands/get_command.py`**: Extraction de la logique de la commande `get` dans son propre fichier.

- **`src/commands/list_command.py`**: Extraction de la logique de la commande `list` dans son propre fichier.

- **`src/commands/debug_command.py`**: Extraction de la logique de la commande `debug` dans son propre fichier.

- **`src/shell.py`**: Simplification massive du fichier pour agir comme un dispatcheur dynamique des commandes, chargeant les commandes depuis le dossier `src/commands/`.

## [MISSION 3.1] - 2025-07-08 - par Manus

### Objectif de la Phase

Amélioration de l'affichage des détails pour la commande `get` et enrichissement des données avec les ports réseau.

### Modifications Apportées

- **`src/shell.py`**:
  - Refonte de l'affichage de la commande `get` pour présenter les informations générales et les ports réseau dans des tables `rich` distinctes, encapsulées dans un `Panel` global.
  - Suppression de l'ancienne table clé-valeur.
  - Ajout d'une logique pour vérifier la présence de ports réseau et les afficher si disponibles.

## [MISSION 2.10] - 2025-07-08 - par Manus

### Objectif de la Phase

Correction finale de la méthode de recherche `search_item` pour extraire correctement l'ID de l'objet en se basant sur la réponse réelle de l'API GLPI.

### Modifications Apportées

- **`src/api_client.py`**:
  - Modification des `params` de la requête `search_item` pour inclure `forcedisplay[0]=2`, assurant que l'ID de l'objet est toujours présent dans la réponse.
  - Correction de la logique d'analyse de la réponse JSON pour rechercher la clé `"2"` pour l'ID de l'objet.
  - Ajout d'un bloc `try...except` plus robuste pour gérer les erreurs de parsing JSON ou les structures de données inattendues.

## [MISSION 2.8] - 2025-07-08 - par Manus

### Objectif de la Phase

Correction de la construction de la requête de recherche dans `search_item` pour assurer la compatibilité avec l'API GLPI.

### Modifications Apportées

- **`src/api_client.py`**:
  - Remplacement de la définition du dictionnaire `params` par une liste de tuples pour `search_item` afin de garantir l'ordre et l'encodage correct des clés complexes.
  - Ajout de `forcedisplay[0]=2` pour forcer le retour de l'ID de l'objet.
  - Ajustement de l'analyse de la réponse JSON pour utiliser la structure prévisible avec `forcedisplay`.

## [MISSION 2.7] - 2025-07-08 - par Manus

### Objectif de la Phase

Création d'un script de test API autonome pour diagnostiquer les problèmes de recherche et de listing.

### Modifications Apportées

- **`test_api.py`**: Nouveau script Python autonome pour tester la connexion à l'API GLPI, lister des itemtypes et rechercher des objets spécifiques. Le script utilise `rich` pour des logs clairs et ne nécessite aucune interaction utilisateur.

## [MISSION 2.6] - 2025-07-08 - par Manus

### Objectif de la Phase

Correction des bugs des commandes `list` et `get`.

### Modifications Apportées

- **`src/shell.py`**:
  - Correction des mappings pour `PassiveDevice` vers `PassiveEquipment` pour les alias `patchpanel`, `patch`, `pp`, `walloutlet`, `wo`.

- **`src/api_client.py`**:
  - Refactorisation de la logique d'extraction de l'ID dans `search_item` pour gérer la structure de réponse de l'API GLPI avec `totalcount` et les clés numériques (`'2'`) pour l'ID.

## [MISSION 2.5] - 2025-07-08 - par Manus

### Objectif de la Phase

Amélioration de l'aide contextuelle pour la commande `list` et modernisation du style du tableau de résultats.

### Modifications Apportées

- **`src/shell.py`**:
  - Ajout d'une aide contextuelle pour la commande `list` lorsqu'elle est appelée sans argument, affichant les types d'objets disponibles et leurs alias dans une table `rich`.
  - Amélioration du style de la table de résultats de la commande `list` en utilisant des bords arrondis (`box.ROUNDED`), un en-tête stylisé (`bold magenta`), et un titre stylisé (`bold blue`).

## [MISSION 2.4] - 2025-07-08 - par Manus

### Objectif de la Phase

Amélioration du shell avec historique des commandes.

### Modifications Apportées

- **`requirements.txt`**: Ajout de la dépendance `prompt-toolkit`.

- **`src/shell.py`**: Remplacement de `rich.console.Console.input()` par `prompt_toolkit.PromptSession` pour offrir un historique des commandes et une meilleure expérience d'édition.

## [MISSION 2.3] - 2025-07-05 - par Manus

### Objectif de la Phase

Correction de la logique d'analyse des arguments pour la commande `get` afin de séparer correctement le type d'objet de son nom.

### Modifications Apportées

- **`src/shell.py`**: Refonte de la logique de parsing des arguments pour la commande `get`. Utilisation de `split(maxsplit=1)` pour extraire le type et le nom de l'objet, même si le nom contient des espaces. Ajout de validations pour les arguments manquants et les types d'objets inconnus.

## [MISSION 2.2.1] - 2025-07-05 - par Manus

### Objectif de la Phase

Correction d'une `SyntaxError` dans `src/shell.py` due à un bloc `try...except` mal structuré.

### Modifications Apportées

- **`src/shell.py`**: Restauration de la structure `try...except` correcte dans la méthode `run()` pour assurer la bonne exécution de l'application. Le bloc `except EOFError:` a été réaligné correctement avec le bloc `try`.

## [MISSION 2.2] - 2025-07-05 - par Manus

### Objectif de la Phase

Implémentation de la commande `list <type>` pour lister les équipements GLPI avec pagination par défaut.

### Modifications Apportées

- **`src/api_client.py`**:
  - Ajout d'une nouvelle méthode `list_items(self, itemtype, item_range="0-4")` pour effectuer des requêtes GET paginées vers le endpoint `/apirest.php/{itemtype}/`.
  - La méthode inclut les paramètres `range` et `expand_dropdowns`.

- **`src/shell.py`**:
  - Ajout de la gestion de la commande `list` dans la méthode `run()`.
  - Validation de la présence de l'argument `<type>`.
  - Utilisation de `TYPE_ALIASES` pour traduire l'alias utilisateur en `itemtype` GLPI.
  - Appel de la méthode `api_client.list_items` pour récupérer les données.
  - Affichage des résultats dans une `rich.table.Table` avec les colonnes "ID", "Nom" et "Statut", encapsulée dans un `Panel`.

## [MISSION 2.1] - 2025-07-05 - par Manus

### Objectif de la Phase

Refonte de la commande `get` pour exiger la spécification du type d'objet, simplifiant la logique de recherche et augmentant la fiabilité.

### Modifications Apportées

- **`src/shell.py`**:
  - La commande `get` accepte désormais deux arguments : le type et le nom de l'objet (`get <type> <nom_objet>`).
  - Ajout d'une validation pour s'assurer que deux arguments sont fournis, avec un message d'erreur clair si ce n'est pas le cas.
  - Implémentation d'un dictionnaire `TYPE_ALIASES` pour mapper les alias utilisateur (`computer`, `pc`, etc.) aux `itemtypes` GLPI réels (`Computer`, `NetworkEquipment`, etc.).
  - Validation de l'alias de type fourni par l'utilisateur.
  - Adaptation de l'appel à `api_client.search_item` pour utiliser le `itemtype` et le `item_name` extraits.

- **`src/api_client.py`**:
  - Renommage de la méthode `search_item_by_name` en `search_item`.
  - Modification de la signature de `search_item` pour accepter `itemtype` et `item_name`.
  - Suppression de la boucle interne qui itérait sur différents types d'objets ; la méthode effectue désormais une seule requête sur l' `itemtype` fourni.
  - La méthode `search_item` retourne maintenant uniquement l'ID de l'item trouvé, ou `None`.

## [MISSION 1.6] - 2024-07-05 - par Manus

### Objectif de la Phase

Refactorisation de la méthode de recherche d'items pour aligner la logique sur l'ancienne méthode fonctionnelle.

### Modifications Apportées

- **`src/api_client.py`**:
  - Modifié la méthode `search_item_by_name` pour utiliser les noms de champs littéraux (`'name'`) au lieu des ID numériques dans les critères de recherche.
  - Amélioré l'analyse de la réponse JSON pour gérer les cas où la clé `data` est présente ou lorsque la réponse est directement une liste, assurant une robustesse accrue face aux variations de l'API.

## [MISSION 1.5] - 2024-07-05 - par Manus

### Objectif de la Phase

Correction de la logique de configuration et de la méthode de recherche API.

### Modifications Apportées

- **`src/api_client.py`**:
  - Corrigé le nom de la clé de configuration de `api_url` à `url`.
  - Corrigé l'en-tête d'authentification pour utiliser `Session-Token` au lieu de `Authorization` pour les requêtes post-connexion.
  - Réécriture complète de la méthode `search_item_by_name` pour qu'elle itère sur les `itemtypes` et interroge le bon endpoint (`/apirest.php/{itemtype}/`) conformément à la documentation de l'API.

## [MISSION 1.4] - 2024-07-05 - par Manus

### Objectif de la Phase

Fiabiliser le chargement de la configuration pour gérer les fichiers corrompus ou incomplets.

### Modifications Apportées

- **`src/shell.py`**: Refonte de la logique de démarrage. L'application ne vérifie plus seulement l'existence du fichier de configuration, mais aussi sa validité (présence et contenu des clés `url`, `app_token`, `user_token`). Si la configuration est invalide, l'assistant de configuration est automatiquement relancé. Ajout d'une méthode d'aide privée `_is_config_valid` pour encapsuler cette logique.

## [MISSION 1.3] - 2024-07-05 - par Manus

### Objectif de la Phase

Refactoring du client API pour une gestion correcte et encapsulée du `session_token`.

### Modifications Apportées

- **`src/api_client.py`**: Le fichier a été entièrement réécrit pour avoir une seule classe `ApiClient`. La classe gère maintenant son propre `session_token` en interne après une connexion réussie. Les méthodes n'ont plus besoin de recevoir le token en paramètre.

- **`src/shell.py`**: Mise à jour de toute la logique pour s'adapter au nouveau `ApiClient`. Le `session_token` n'est plus géré par le shell mais par le client API. La logique de connexion, de test, d'appel des commandes et de déconnexion a été simplifiée.

## [MISSION 1.2] - 2024-07-05 - par Manus

### Objectif de la Phase

Fiabiliser le shell contre les entrées vides et améliorer la robustesse de la commande `get`.

### Modifications Apportées

- **`src/shell.py`**: Ajout d'une vérification pour ignorer les entrées vides, prévenant ainsi le crash `IndexError`. Amélioration de l'affichage des détails pour extraire les noms lisibles du statut et de la localisation.

- **`src/api_client.py`**: Modification de la méthode de recherche pour utiliser `searchtype="contains"` au lieu de `"equals"`, rendant la recherche d'objets plus flexible et efficace.

## [CORRECTION] - 2024-07-05 - par Manus

### Objectif de la Phase

Correction des erreurs de syntaxe dans `src/shell.py`.

### Modifications Apportées

- **`src/shell.py`**: Correction des f-strings non terminées aux lignes 67 et 73 pour résoudre le `SyntaxError: unterminated f-string literal`.

## [MISSION 1.1] - 2024-07-04 - par Manus

### Objectif de la Phase

Implémenter la première commande fonctionnelle `get <nom_objet>` pour rechercher un équipement et afficher ses détails de base.

### Modifications Apportées

- **`src/api_client.py`**: Ajout des méthodes `search_item_by_name` et `get_item_details` pour interagir avec les endpoints de recherche et de récupération d'items de GLPI, en se basant sur la documentation de l'API fournie.

- **`src/shell.py`**: Mise à jour de la boucle principale pour analyser les commandes utilisateur. Implémentation de la logique pour la commande `get`, incluant la recherche, la récupération des détails et l'affichage formaté des résultats dans un `Panel` et une `Table` `rich`.

## [MISSION 0.3.1] - 2024-07-04 - par Manus

### Objectif de la Phase

Correction et fiabilisation de la connexion API et du processus de configuration.

### Modifications Apportées

- **Correction (Mission 0.3.1)**: Fiabilisation du client API, suppression du code en double, et amélioration de la gestion des erreurs de connexion.

## [MISSION 0.3] - 2024-05-24 - par Manus

### Objectif de la Phase

Remplacer la configuration par fichier .env par un processus de configuration interactif et persistant au premier lancement de l'application.

### Modifications Apportées

- **`requirements.txt`**: Suppression de `python-dotenv`.

- **`src/config_manager.py`**: Création du module pour gérer la lecture, l'écriture et la collecte interactive des informations de configuration dans `~/.config/glpi-explorer/config.json`.

- **`src/api_client.py`**: Mise à jour de la classe `ApiClient` pour qu'elle soit initialisée avec un dictionnaire de configuration et pour qu'elle retourne des informations plus détaillées sur l'échec/succès de la connexion.

- **`src/shell.py`**: Refonte majeure de la logique de démarrage pour gérer le flux de configuration : vérifier si la configuration existe, lancer l'assistant interactif si nécessaire, tester et sauvegarder la configuration, puis se connecter à l'API.

## [MISSION 0.2] - 2024-05-24 - par Manus

### Objectif de la Phase

Intégrer la logique de connexion à l'API REST de GLPI, en utilisant un fichier de configuration .env pour les identifiants et en gérant le cycle de vie de la session (init/kill).

### Modifications Apportées

- **`.env.example`**: Création d'un fichier d'exemple pour les variables de configuration de l'API.

- **`requirements.txt`**: Ajout de la dépendance `requests`.

- **`src/config.py`**: Création du module pour charger et valider la configuration depuis le fichier `.env`.

- **`src/api_client.py`**: Implémentation de la classe `ApiClient` avec les méthodes `connect()` et `close_session()`.

- **`src/shell.py`**: Mise à jour du shell pour initier la connexion au démarrage, gérer les échecs et fermer la session en quittant.

## [MISSION 0.1] - 2024-05-24 - par Manus

### Objectif de la Phase

Mise en place du socle de l'application CLI interactive, de sa structure de fichiers et de sa boucle de commande principale.

### Modifications Apportées

- **`glpi-explorer/`**: Création de l'arborescence initiale du projet.

- **`requirements.txt`**: Ajout des dépendances `rich` et `python-dotenv`.

- **`.gitignore`**: Configuration initiale pour les projets Python.

- **`main.py`**: Création du point d'entrée qui lance le shell interactif.

- **`src/shell.py`**: Implémentation de la classe `GLPIExplorerShell` avec une boucle de commande, un message de bienvenue, un prompt stylisé et la logique pour quitter (`exit`/`quit`).
