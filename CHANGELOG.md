## [MISSION 14.4] - 2025-07-17

### Changed
- **fix(cache):** Correction de la liaison NetworkPort-Socket
  - La logique de liaison dans `build_topology_graph` a été corrigée pour se baser sur la clé `networkports_id` présente dans les objets `Socket`.
  - La liaison se fait maintenant en partant du Socket pour trouver son Port logique, ce qui correspond à la structure de données de l'API.
  - Cette modification résout le bug où la trace s'arrêtait après la première étape car le lien entre le port logique et le port physique n'était pas établi.

Ref: Mission 14.4

## [MISSION 14.3] - 2025-07-17

### Changed
- **refactor(cache)!:** Implémentation du constructeur de graphe de topologie final
  - Remplacement de `_link_topology` par une méthode unifiée `build_topology_graph`.
  - Cette méthode établit les liaisons dans un ordre séquentiel strict pour garantir la cohérence : Equipement->Port, Port->Socket, Socket->Câble.
  - La commande `trace` a été réécrite pour naviguer sur ce graphe fiable.
  - Cette approche résout les problèmes de liaison en cascade et constitue la base finale pour la commande `trace`.

BREAKING CHANGE: La logique de liaison et la structure des objets dans le cache ont été modifiées.

Ref: Mission 14.3

## [MISSION 14.2] - 2025-07-17

### Changed
- **fix(cache):** Correction finale de la logique de liaison de topologie
  - Réécriture de `_link_topology` pour utiliser les données riches (`_networkports`) des équipements afin de garantir une liaison Parent->Port fiable.
  - La liaison est maintenant hiérarchique et correcte : Equipement -> NetworkPort -> Socket -> Câble.
  - Cette modification résout les problèmes de "Parent Inconnu" et de points de départ incorrects pour la commande `trace`.

Ref: Mission 14.2

## [MISSION 14.1] - 2025-07-17

### Changed
- **feat(trace):** Implémentation finale de la trace avec traversée des passifs
  - Correction de la logique de liaison dans `_link_topology` pour gérer les `items_id` textuels et numériques.
  - Correction de la recherche des sockets de départ dans `TraceCommand`.
  - Implémentation de la logique de "traversée" pour les équipements passifs (Walloutlets, Patch Panels) en se basant sur la convention de nommage IN/OUT des ports.
  - La commande `trace` est maintenant capable de suivre un chemin complet à travers l'infrastructure physique.

Ref: Mission 14.1

## [MISSION 13.11] - 2025-07-17

### Changed
- **fix(cache):** Correction de l'indexation basée sur le nom des parents
  - La logique de création de l'index `equipment_to_sockets_map` gère maintenant le cas où l'API retourne un nom textuel au lieu d'un ID numérique pour le parent d'un socket.
  - Cette modification résout la cause racine de l'échec de la liaison équipement-socket.
- **feat(debug):** Ajout de la commande 'debug index'
  - Création de la commande `debug index` pour afficher le contenu de la map `equipment_to_sockets_map`.
  - Cet outil permet de valider visuellement que l'index est construit correctement.

Ref: Mission 13.11

## [MISSION 13.10] - 2025-07-17

### Changed
- **feat(cache):** Création d'un index Équipement-vers-Sockets
  - Abandon de la liaison par attribut au profit d'une structure d'indexation dédiée `equipment_to_sockets_map`.
  - Le cache crée maintenant une map `[equipment_id] -> [socket_id_1, socket_id_2, ...]` lors du chargement.
  - Ajout d'une méthode `get_sockets_for_item_id` pour interroger cet index de manière propre.
  - La commande `trace` a été mise à jour pour utiliser cette nouvelle méthode, rendant la recherche des points de départ fiable et explicite.

Ref: Mission 13.10

## [MISSION 13.9] - 2025-07-16

### Changed
- **refactor(cache)!:** Simplification de la topologie basée sur la liaison Équipement-Socket.
  - La logique de liaison du cache a été refondue pour créer une relation directe entre un Équipement et ses Sockets physiques.
  - Abandon de la dépendance complexe aux NetworkPorts pour la construction de la topologie de base.
  - Chaque objet équipement dans le cache possède maintenant un attribut `sockets` qui est une liste de ses objets socket.
  - La commande `trace` a été adaptée pour utiliser cette nouvelle structure simple et robuste.

## [MISSION 13.10] - 2025-07-16

### Changed
- **feat(trace)::** Implémentation fonctionnelle de la commande trace.
  - La commande `trace` a été corrigée pour utiliser le bon attribut (`.ports`) des objets du cache.
  - La logique de navigation complexe a été centralisée dans une nouvelle méthode `build_path_from_item` du `TopologyLinker`.
  - La commande `trace` est maintenant fonctionnelle et capable de suivre une connexion physique de base.

## [MISSION 13.9] - 2025-07-16

### Changed
- **feat(display):** Finalisation de l'affichage 'get' via le cache structuré.
  - La commande `get` a été mise à jour pour lire le nouvel attribut `item.ports` des objets du cache.
  - La logique de parsing complexe a été supprimée de la commande, qui se contente maintenant de parcourir une liste simple d'objets "port".
  - L'affichage des détails d'un équipement et de ses ports est maintenant pleinement fonctionnel et robuste.

## [MISSION 13.8] - 2025-07-16

### Changed
- **refactor(cache):** Aplatissement structuré des données de ports.
  - Le processus de chargement du cache transforme maintenant la structure `_networkports` complexe de l'API en une simple liste d'objets attachée à chaque équipement (`equip.ports`).
  - Chaque objet de cette liste contient les informations clés d'un port (id, nom, vitesse, etc.).
  - Cette approche simplifie radicalement l'accès aux données de ports pour toutes les commandes, en particulier `get` et la future commande `trace`.

## [MISSION 13.5] - 2025-07-16

### Changed
- **perf(commands):** Refonte des commandes `list`, `get`, et `compare` pour l'utilisation exclusive du cache.
  - Les commandes n'effectuent plus d'appels API directs.
  - Toutes les données sont maintenant lues instantanément depuis le `TopologyCache` local.
  - Amélioration drastique de la performance et de la réactivité de l'application après le chargement initial.

## [MISSION 13.3] - 2025-07-16 - par Gemini

### Objectif de la Phase

Implémentation de la commande trace avec logique de traversée.

### Modifications Apportées

- **`src/topology_linker.py`**:
    - Le `TopologyLinker` gère maintenant la traversée des équipements passifs (IN->OUT) et la logique de concentration des hubs.
    - La méthode principale `get_next_hop` orchestre la navigation de socket en socket.
- **`src/commands/trace_command.py`**:
    - La commande `trace` a été réactivée et réécrite pour utiliser le `TopologyLinker`.
    - L'outil est maintenant capable de tracer un chemin réseau complet.

### Justification Technique

Cette mission établit la logique de traçage complète dans le `TopologyLinker` et la rend disponible à travers la commande `trace`.

Ref: Mission 13.3

## [MISSION 13.2] - 2025-07-16 - par Gemini

### Objectif de la Phase

Création du `TopologyLinker` et de la navigation de base.

### Modifications Apportées

- **`src/topology_linker.py`**:
    - Création de la nouvelle classe `TopologyLinker` qui encapsule la logique de navigation dans le cache.
    - Implémentation des méthodes de recherche de base : `find_item`, `find_socket_by_id`, et `find_connection_for_socket`.
- **`src/commands/testlink_command.py`**:
    - Ajout d'une commande de test `testlink <socket_id>` pour valider le bon fonctionnement de la liaison Socket-Câble-Socket via le linker.

### Justification Technique

Cette mission établit le "cerveau" de notre nouvelle architecture.

Ref: Mission 13.2

## [MISSION 13.1] - 2025-07-16 - par Gemini

### Objectif de la Phase

Refonte du Cache en Dépôt de Données Brutes.

### Modifications Apportées

- **`src/topology_cache.py`**:
    - Suppression complète de la méthode `_link_topology` et de toute logique de liaison implicite au chargement.
    - Le TopologyCache agit désormais comme un simple conteneur de données, chargeant les objets bruts depuis l'API.
- **`src/commands/trace_command.py`**:
    - La commande `trace` est temporairement désactivée pour éviter les crashs suite à la refonte du cache.
- **`src/commands/get_command.py`**:
    - La sous-commande `get port` est temporairement désactivée.

### Justification Technique

Cette modification est la première étape de la nouvelle architecture découplée (Dépôt/Linker) et prépare le terrain pour la création d'un `TopologyLinker` dédié.

BREAKING CHANGE: La structure et le rôle du cache ont été fondamentalement modifiés.

Ref: Mission 13.1

## [MISSION 12.8] - 2025-07-16 - par Gemini

### Objectif de la Phase

Correction de l'affichage du panneau de démarrage pour un rendu final unifié et compact.

### Modifications Apportées

- **`src/topology_cache.py`**:
    - Abandon de `rich.Layout` au profit de `rich.Group` pour un contrôle plus flexible de l'affichage.
    - Le logo et la barre de progression sont groupés et affichés dans un seul `Panel` via `rich.Live`.
    - Une fois le chargement terminé, le `Live` est mis à jour pour remplacer la barre de progression par le message de bienvenue et la version, le tout dans le même `Panel` qui se redimensionne automatiquement.

### Justification Technique

Cette modification finale corrige le problème de l'espace vertical excessif et assure un affichage de démarrage unifié et compact, comme demandé.

Ref: Mission 12.8

## [MISSION 12.7] - 2025-07-16 - par Gemini

### Objectif de la Phase

Correction de l'affichage du panneau de démarrage pour éviter les panneaux doubles.

### Modifications Apportées

- **`src/shell.py`**:
    - Suppression de l'affichage du panneau de bienvenue.
- **`src/topology_cache.py`**:
    - Modification de la méthode `load_from_api` pour intégrer le message de bienvenue et la version dans le panneau de chargement après la fin du chargement.

### Justification Technique

Cette modification centralise l'affichage du démarrage dans `topology_cache.py`, évitant ainsi l'affichage de deux panneaux successifs et offrant une expérience utilisateur plus propre et plus professionnelle.

Ref: Mission 12.7

## [MISSION 12.6] - 2025-07-16 - par Gemini

### Objectif de la Phase

Amélioration de l'affichage du panneau de démarrage pour qu'il persiste après le chargement.

### Modifications Apportées

- **`src/topology_cache.py`**:
    - Suppression de l'argument `screen=True` de `rich.Live` pour que le panneau reste visible après le chargement.
    - Utilisation de `rich.align.Align.center` pour centrer le panneau et limiter sa largeur à celle du logo.
    - Ajout d'une mise à jour finale à la barre de progression pour afficher un message de "chargement terminé".

### Justification Technique

Cette modification garantit que le panneau de démarrage avec le logo persiste à l'écran après le chargement, offrant une expérience utilisateur plus cohérente et esthétique.

Ref: Mission 12.6

## [MISSION 12.5] - 2025-07-16 - par Gemini

### Objectif de la Phase

Intégration du logo ASCII et de la barre de progression dans un seul panneau.

### Modifications Apportées

- **`src/topology_cache.py`**:
    - La méthode `load_from_api` a été modifiée pour utiliser `rich.Live` et `rich.Layout`.
    - Le logo ASCII "GLPI-Explorer" et la barre de progression sont maintenant affichés dans un seul `Panel` unifié.
    - La barre de progression est mise à jour dynamiquement à l'intérieur du panneau sans réimprimer tout l'écran.

### Justification Technique

Cette modification améliore encore l'esthétique du panneau de démarrage en intégrant le logo et la barre de progression dans un seul cadre, offrant une expérience utilisateur plus professionnelle et plus propre.

Ref: Mission 12.5

## [MISSION 12.4] - 2025-07-16 - par Gemini

### Objectif de la Phase

Amélioration de l'esthétique du panneau de démarrage.

### Modifications Apportées

- **`src/topology_cache.py`**:
    - Refonte complète de la méthode `load_from_api` pour améliorer l'esthétique du panneau de démarrage.
    - Le chargement se fait maintenant en deux passes : d'abord, récupération de tous les ID pour calculer le total, puis chargement des détails.
    - Utilisation d'un `Panel` `rich` unique avec le titre "GLPI-Explorer".
    - Utilisation d'une seule barre de progression `rich` qui affiche le décompte des équipements en cours de chargement (par exemple, "Chargement Computers: 12/153").
    - Suppression des anciennes méthodes de chargement individuelles (`_load_computers`, etc.).

### Justification Technique

Cette modification améliore considérablement l'expérience utilisateur au démarrage de l'application, en fournissant un retour visuel plus clair, plus esthétique et plus informatif, similaire à celui de Gemini CLI.

Ref: Mission 12.4

## [MISSION 12.3] - 2025-07-16 - par Gemini

### Objectif de la Phase

Création d'un script de validation de la liaison "Socket-Câble-Socket".

### Modifications Apportées

- **`link_validator.py`**:
    - Création d'un script de diagnostic autonome pour valider la capacité à suivre une connexion physique de base (`Socket -> Câble -> Socket`) en utilisant les données du cache.
    - Le script prend un ID de socket en argument de ligne de commande, charge le cache de topologie complet, et tente de trouver le câble connecté et l'autre socket à l'extrémité.
    - Affiche un rapport de diagnostic détaillé de chaque étape.

### Justification Technique

Ce script est une étape de validation cruciale avant de refondre l'architecture de la commande `trace`. Il permet de s'assurer que le cache contient les informations correctes et que la logique de base de la liaison est fonctionnelle.

Ref: Mission 12.3

## [MISSION 12.2] - 2025-07-15 - par Gemini

### Objectif de la Phase

Correction de la Référence d'Objet dans la Commande "trace"

### Modifications Apportées

- **`src/commands/trace_command.py`**:
    - Réécriture complète de la commande pour résoudre le problème de référence d'objet.
    - La recherche de l'objet de départ se fait maintenant directement dans la commande, sans méthode d'aide, pour garantir la manipulation de l'objet enrichi du cache.
    - L'accès aux ports se fait via `getattr(start_item, 'networkports', [])` pour gérer le cas où l'attribut n'existerait pas.

### Justification Technique

Cette modification résout l'AttributeError et rend la commande `trace` fonctionnelle.

Ref: Mission 12.2

## [MISSION 12.1] - 2025-07-15 - par Gemini

### Objectif de la Phase

Implémentation Finale de la Logique de Traçage Complète

### Modifications Apportées

- **`src/commands/trace_command.py`**:
    - Refonte totale de la commande `trace` pour naviguer sur le cache de topologie.
    - La navigation se base sur la hiérarchie Équipement -> NetworkPort -> Socket.
    - Ajout d'une logique de "traversée" interne pour les équipements passifs (IN -> OUT).
    - Ajout d'une logique de "concentration" pour les hubs (IN -> port OUT principal).
- **`src/topology_cache.py`**:
    - Ajout de la méthode d'aide `find_socket_by_name`.

### Justification Technique

La commande `trace` est maintenant fonctionnelle et capable de suivre un chemin réseau complexe.

Ref: Mission 12.1

## [MISSION 11.6] - 2025-07-15 - par Gemini

### Objectif de la Phase

Finalisation de la Commande "trace" et Amélioration du Chargement

### Modifications Apportées

- **`src/commands/trace_command.py`**:
    - La commande `trace` a été corrigée pour lire les ports directement depuis l'attribut `_networkports` des objets du cache, résolvant l'AttributeError.
    - La logique de traçage est maintenant pleinement fonctionnelle sur le cache riche.
- **`src/topology_cache.py`**:
    - La barre de progression au démarrage a été améliorée pour afficher des descriptions claires de chaque étape de chargement.
    - Suppression des méthodes de recherche obsolètes.

### Justification Technique

Cette mission finalise la fonctionnalité de traçage en l'alignant sur la nouvelle structure de cache riche et améliore l'expérience utilisateur lors du chargement initial.

Ref: Mission 11.6

## [MISSION 11.5] - 2025-07-15 - par Gemini

### Objectif de la Phase

Refonte du Chargement du Cache par "Get Details" Individuel

### Modifications Apportées

- **`src/api_client.py`**:
    - Ajout du paramètre `only_id=True` par défaut à la méthode `list_items` pour optimiser la récupération des listes d'ID.
- **`src/topology_cache.py`**:
    - Le processus de chargement du cache a été entièrement réécrit.
    - Il ne se base plus sur les réponses allégées de `list_items`, mais effectue un `get_item_details` pour chaque objet individuel du parc.
    - Cette approche garantit que les objets dans le cache sont aussi riches et complets que ceux affichés par la commande 'get'.
    - La méthode `_link_topology` a été simplifiée pour ne gérer que la liaison des câbles.

### Justification Technique

Bien que plus lent au premier chargement, ce mécanisme résout définitivement le problème des attributs manquants (comme `_networkports`) et assure la fiabilité du cache.

Ref: Mission 11.5

## [MISSION 11.4] - 2025-07-15 - par Gemini

### Objectif de la Phase

Refonte du Cache par Enrichissement HATEOAS

### Modifications Apportées

- **`src/api_client.py`**:
    - Ajout d'une nouvelle méthode `get_sub_items(self, full_href)` pour suivre les liens HATEOAS.
- **`src/topology_cache.py`**:
    - La création du cache se fait maintenant en deux passes : chargement brut, puis enrichissement.
    - La liaison Équipement-NetworkPort se base désormais sur le suivi des liens HATEOAS (`rel: "NetworkPort"`) fournis par l'API.
    - La méthode `load_from_api` a été simplifiée.
    - La méthode `_link_topology` a été entièrement réécrite pour implémenter la nouvelle logique d'enrichissement.
    - Suppression des anciennes méthodes de recherche (`get_ports_for_item`, `get_socket_for_port`, etc.) devenues obsolètes.

### Justification Technique

Cette approche garantit que chaque équipement dans le cache contient une liste complète et fiable de ses ports, en se basant directement sur les informations fournies par l'API (HATEOAS). Cela élimine les erreurs de liaison dues aux incohérences de l'API.

Ref: Mission 11.4

## [MISSION 11.3] - 2025-07-15 - par Gemini

### Objectif de la Phase

Refonte du Cache avec Méthodes de Recherche Explicites

### Modifications Apportées

- **`src/topology_cache.py`**:
    - Abandon de la méthode `_link_topology` qui attachait des attributs aux objets du cache.
    - Création de méthodes de recherche explicites dans `TopologyCache` (`get_ports_for_item`, `get_socket_for_port`, etc.).
- **`src/commands/trace_command.py`**:
    - La commande `trace` a été réécrite pour utiliser ces nouvelles méthodes.

### Justification Technique

Cette approche est plus robuste, plus facile à déboguer et élimine les problèmes de "magie" qui échouaient silencieusement.

BREAKING CHANGE: La manière d'interagir avec le cache a été complètement modifiée.

## [MISSION 11.2] - 2025-07-15 - par Gemini

### Objectif de la Phase

Correction de la liaison Équipement-NetworkPort par nom.

### Modifications Apportées

- **`src/topology_cache.py`**:
    - La méthode `_link_topology` gère maintenant le cas où l'API GLPI retourne le nom de l'équipement parent au lieu de son ID dans le champ `items_id` d'un objet NetworkPort.
    - La liaison se fait désormais soit par ID numérique, soit par nom, ce qui résout la cause racine de l'échec de la commande `trace`.

### Justification Technique

Cette modification finale corrige la cause racine de l'échec de la commande `trace`.

## [MISSION 11.1] - 2025-07-15 - par Gemini

### Objectif de la Phase

Script de Diagnostic du Processus de Création du Cache

### Modifications Apportées

- **`cache_builder_diagnostic.py`**:
    - Création d'un script de diagnostic pour isoler et tester la logique de liaison des objets dans le cache.

### Justification Technique

Cet outil est conçu pour identifier la cause exacte de l'échec de l'attachement des `NetworkPorts` à leurs équipements parents.

## [MISSION 10.7] - 2025-07-15 - par Gemini

### Objectif de la Phase

Refonte finale de la liaison de topologie hiérarchique.

### Modifications Apportées

- **`src/topology_cache.py`**:
    - Réécriture complète de `_link_topology` pour établir une chaîne de liaison fiable basée sur la structure avérée de l'API GLPI.
    - La liaison se fait désormais dans cet ordre : Équipement -> NetworkPort, puis NetworkPort -> Socket.
    - La liaison du Socket à son parent se fait maintenant via la parenté de son NetworkPort, résolvant les incohérences de l'API.

### Justification Technique

Cette modification finale corrige la cause racine de l'échec de la commande `trace`.

## [MISSION 10.6] - 2025-07-15 - par Gemini

### Objectif de la Phase

Refonte finale de la liaison de topologie.

### Modifications Apportées

- **`src/topology_cache.py`**:
    - Réécriture complète de `_link_topology` pour établir une chaîne de liaison hiérarchique et fiable : Équipement -> NetworkPort -> Socket.

### Justification Technique

Cette modification corrige la cause racine de l'échec de `trace` en assurant que chaque équipement est correctement associé à ses ports et sockets.

## [MISSION 10.5] - 2025-07-15 - par Gemini

### Objectif de la Phase

Correction de la commande `debug cache` pour accepter les noms d'équipement.

### Modifications Apportées

- **`src/commands/debug_command.py`**:
    - La méthode `execute` a été modifiée pour accepter un nom d'équipement en plus d'un ID.
    - Ajout de la méthode `_display_item_details_by_name` pour rechercher un équipement par nom dans le cache.

### Justification Technique

La commande `debug cache` ne fonctionnait qu'avec des ID numériques, ce qui la rendait difficile à utiliser. Cette modification permet aux utilisateurs de spécifier un nom d'équipement, ce qui est plus intuitif et pratique.

## [MISSION 10.4] - 2025-07-15 - par Gemini

### Objectif de la Phase

Correction de la logique de liaison Équipement-NetworkPort.

### Modifications Apportées

- **`src/topology_cache.py`**:
    - Correction de la logique dans `_link_topology` pour utiliser le `itemtype` de l'équipement parent lors de la liaison des `NetworkPort`.

### Justification Technique

La logique précédente utilisait incorrectement le `itemtype` du `NetworkPort` lui-même, ce qui empêchait la liaison correcte avec son équipement parent. Cette correction assure que la liaison est maintenant correctement établie.

## [MISSION 10.3] - 2025-07-14 - par Gemini

### Objectif de la Phase

Correction Finale de la Liaison Équipement-NetworkPort

### Modifications Apportées

- **`src/topology_cache.py`**:
    - La méthode `_link_topology` a été mise à jour pour parcourir tous les `NetworkPort` du cache et les attacher à leur équipement parent.
    - Chaque objet équipement (Computer, Switch...) possède maintenant un attribut `networkports` qui est une liste de ses objets port.

### Justification Technique

Cette correction résout le problème où la commande `trace` ne trouvait aucun port de départ sur un équipement.

## [MISSION 10.2] - 2025-07-14 - par Gemini

### Objectif de la Phase

Correction de la Liaison Parent-Socket via le Nom

### Modifications Apportées

- **`src/topology_cache.py`**:
    - La méthode `_link_topology` gère maintenant le cas où l'API GLPI retourne le nom de l'équipement parent au lieu de son ID dans le champ `items_id` d'un objet Socket.
    - La liaison se fait désormais en priorité par ID numérique, et en fallback par nom (insensible à la casse), rendant le processus beaucoup plus robuste.
- **`src/commands/trace_command.py`**:
    - La commande 'trace' a été adaptée pour trouver les sockets de départ en se basant sur l'attribut `parent_item`.

### Justification Technique

Cette modification résout la cause racine de l'échec de la commande `trace`.

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

- Le cache charge désormais les `Glpi\Socket` en plus des autres équipements.
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
    - Implémentation d'une nouvelle méthode `_load_sockets` pour charger tous les objets `Glpi\Socket` depuis l'API.
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
  - Correction de la logique d'analyse de la réponse JSON pour rechercher la clé "2" pour l'ID de l'objet.
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
  - Refactorisation de la logique d'extraction de l'ID dans `search_item` pour gérer la structure de réponse de l'API GLPI avec `totalcount` et les clés numériques ("2") pour l'ID.

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