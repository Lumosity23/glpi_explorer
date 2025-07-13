# Modèle de données réseau GLPI

## 1. Entités manipulées

- **SWITCH** (`SW`)
  - Appareil actif avec plusieurs ports Ethernet (pas nécessairement pairs).
  - Ports nommés : `SW <nom> port n`

- **SOCKET**
  - Interface physique sur un appareil, utilisée pour brancher un câble.
  - Chaque socket est soit `IN` soit `OUT`.

- **PORT ETHERNET**
  - Terme générique pour désigner un point de connexion sur un device (souvent équivalent à un socket, utilisé différemment selon le contexte GLPI).

- **HUB ETHERNET** (`HB`)
  - Passif (dans cette modélisation), un seul port est considéré comme `OUT` (celui avec le plus grand numéro).
  - Autres ports sont `IN`.

- **PATCH PANEL** (`PP`)
  - Passif, avec un nombre pair de ports.
  - Nommage : `PP <nom> port n IN/OUT`

- **ROOM**
  - Salle physique.
  - Dans GLPI, une room est modélisée comme un passive device avec ports `IN` et `OUT`.
  - Nommage : `WO <nom de room> port n IN/OUT`

- **WALLOUTLET** (`WO`)
  - Prise murale RJ45.
  - Nommage : `WO <nom de la room> port n IN/OUT`

- **CABLE** (`C`)
  - Relie deux sockets (ou ports).
  - Syntaxe : `C-<nom du device> port n IN/OUT`

## 2. Règles structurelles

- Tous les **passive devices** doivent avoir un **nombre pair de ports**.
- Pour chaque port `IN`, un port `OUT` correspondant est défini.
- Les liaisons logiques doivent respecter la continuité physique :
  - Exemple : `PC → Walloutlet → Patch Panel → Switch`

- Chaque entité est **identifiée par son type + nom + port**, avec suffixe `IN` ou `OUT`.

- Une liaison se fait toujours entre un `OUT` et un `IN`.

## 3. Objectif de modélisation

- Permettre une **traversée récursive du réseau**, en partant de n’importe quel device (PC ou port de switch), et en suivant les connexions physiques jusqu’à une extrémité logique (autre device ou routeur).

