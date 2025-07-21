# 🚀 GLPI Explorer

**Un outil CLI et une plateforme de visualisation pour explorer, auditer et gérer votre infrastructure réseau directement depuis GLPI.**

![Ecran de demarage de GLPI-Explorer](/DOCS/Screenshot%20from%202025-07-21%2023-03-26.png)

---

## ✨ Vision

GLPI Explorer a pour ambition de transformer la manière dont les administrateurs réseau interagissent avec leur inventaire GLPI. Fini les clics interminables et les recherches fastidieuses. Cet outil offre une interface en ligne de commande (CLI) rapide et puissante, ainsi qu'un éditeur de topologie visuel, pour une gestion de parc intuitive et efficace.

Que ce soit pour un diagnostic rapide, un audit de conformité, ou la conception d'une nouvelle infrastructure, GLPI Explorer est conçu pour être votre co-pilote.

## 🌟 Fonctionnalités Clés

| Fonctionnalité | Statut | Description |
| :--- | :---: | :--- |
| **Shell Interactif** | ✅ **Stable** | Une interface CLI moderne avec historique des commandes et auto-complétion. |
| **Cache de Topologie** | ✅ **Stable** | Chargement initial de tout le parc pour des performances quasi-instantanées. |
| **`list`** | ✅ **Stable** | Lister rapidement tous les équipements d'un type donné (`list pc`, `ls sw`). |
| **`get`** | ✅ **Stable** | Obtenir une vue détaillée et formatée de n'importe quel équipement. |
| **`compare`** | ✅ **Stable** | Comparer deux équipements côte à côte pour une analyse facile. |
| **`trace` (Ascendant)** | ✅ **Stable** | Suivre un chemin réseau complet d'un terminal vers le cœur du réseau. |
| **`map` (Descendant)** | 🚧 **En Développement** | Explorer interactivement les connexions depuis un équipement central. |
| **Cache Dynamique** | 🚧 **En Développement** | `refresh`, `changes` et notifications pour un cache toujours à jour. |
| **Audit & Conformité (`checkup`)** | 🗓️ **Prévu** | Auditer le parc pour détecter les anomalies (câbles orphelins, etc.). |
| **Mode "Constructeur" (`create`, `connect`)** | 🗓️ **Prévu** | Créer et câbler de nouveaux équipements directement depuis le CLI. |
| **Éditeur Visuel (`network-map`)** | 🗓️ **Prévu** | Une interface web pour visualiser et éditer la topologie en glisser-déposer. |

---

## 🛠️ Installation et Utilisation

### Installation

Pour installer GLPI Explorer, utilisez pip avec l'URL du dépôt Git :

```bash
pip install git+https://github.com/Timo-AI/GLPI-Explorer.git
```

Pour mettre à jour vers la dernière version :

```bash
pip install --upgrade git+https://github.com/Timo-AI/GLPI-Explorer.git
```

### Lancement

Une fois installé, vous pouvez lancer l'application de n'importe où avec la commande :

```bash
glpi
```

### Configuration Initiale

Au premier lancement, l'application vous guidera pour configurer les accès à votre API GLPI (URL, App-Token, User-Token). Ces informations sont stockées localement dans `~/.config/glpi-explorer/config.json`.

---

## 🚀 Exemples d'Utilisation

### Lister des équipements
```bash
# Lister les 5 premiers ordinateurs
(glpi-explorer)> list pc
 
```

### Obtenir les détails d'un équipement
```bash
# Afficher les détails du PC nommé "PC-FINANCE-01"
(glpi-explorer)> get pc PC-FINANCE-01

# Afficher les détails d'un port spécifique
(glpi-explorer)> get port Gi1/0/1 on SW-CORE-A01
```

### Tracer un chemin réseau
```bash
# Suivre la connexion depuis un ordinateur jusqu'au switch
(glpi-explorer)> trace pc PC-FINANCE-01
```
*(Le résultat est une table détaillée montrant chaque "saut" à travers les câbles, walloutlets et patch panels.)*

---

## 🗺️ Vision Future : L'Éditeur `network-map`

L'objectif à long terme est d'intégrer un éditeur visuel accessible via la commande `map --serve`. Cette interface permettra de visualiser, de modifier et de construire la topologie réseau de manière intuitive.


![Maquette de l'interface network-map](/DOCS/Screenshot%20from%202025-07-21%2022-49-19.png)

---

*Ce projet est développé dans le cadre d'un projet étudiant, un stage au VKI
