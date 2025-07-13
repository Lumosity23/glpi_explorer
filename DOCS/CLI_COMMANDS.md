# 📟 CLI Commandes - Supervision Réseau via GLPI API

Ce fichier décrit la syntaxe des commandes pour interroger le parc réseau (GLPI) via l’agent IA.

---

## 🔹 Syntaxe générale

- `<objet>` [commande 1] [commande 2] ...
- `<objet>` : nom exact d’un élément dans GLPI (ex. : `pc1`, `SW01`, `WO-B-204`)
- `[commande]` : modificateurs optionnels pour enrichir la requête

---

## 🔸 Objets supportés (éléments GLPI)

- `pc` : ordinateurs
- `sw` : switchs (network devices)
- `hub` : hubs ethernet
- `patch` : patch panels
- `wo` : wall outlets (prise murale)
- `cb` : câbles
- `room` : salles / locaux
- `socket`, `port` : composants d’entrée/sortie

Chaque objet peut être interrogé seul ou avec des commandes supplémentaires.

---

## 🔸 Commandes disponibles

| Commande         | Alias       | Description                                                                 |
|------------------|-------------|-----------------------------------------------------------------------------|
| `expose port`    | `ports`     | Affiche les ports disponibles + connexions                                 |
| `expose socket`  | `sockets`   | Affiche les sockets et liaisons                                            |
| `status`         |             | Retourne l’état GLPI (actif, désactivé, hors-ligne...)                     |
| `room`           | `locate`    | Donne l'emplacement physique (salle)                                       |
| `trace`          | `route`     | Affiche toute la chaîne de connexion (du début à la fin)                   |
| `cable`          | `cb`, `link`| Affiche tous les câbles liés à cet objet                                   |
| `mapping`        |             | Affiche la carte logique (visuelle ou liste) des connexions (utile en salle)|
| `locate`         | `position`  | Donne les coordonnées exactes (physiques ou planifiées)                    |

---

## 🔸 Exemples concrets

### ▶ Commandes de base
```bash
pc1                      → Résumé simple (nom, type, statut, salle)
SW01 expose port         → Liste des ports disponibles du switch SW01
pc2 expose socket status → Affiche les sockets + statut du PC
```

### ▶ Commandes sur câbles
```bash
C-102                    → Infos de base du câble
C-102 trace              → Où il est branché et à quoi
C-102 locate             → Salles ou murs traversés
```

### ▶ Commandes combinées
```bash
pc1 expose port trace
SW01 trace expose port status
WO-B-204 expose socket cable
```