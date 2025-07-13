# Mapping des entités GLPI avec les objets physiques du réseau

## 1. Éléments natifs de GLPI

| Objet réel         | GLPI (type ou section)         | Détail / Remarques                        |
|--------------------|-------------------------------|-------------------------------------------|
| PC / Ordinateur    | Computer                      | Appareil terminal                        |
| Switch             | Network Equipment             | Type = Switch                            |
| Hub Ethernet       | Network Equipment             | Type = Hub (comportement spécial défini) |
| Patch Panel        | Passive Device                | Doit avoir un nombre pair de ports       |
| Walloutlet         | Passive Device                | Nommé selon `WO <Room>`                  |
| Cable              | Cable                         | Lien physique entre deux ports           |
| Room (salle)       | Location                      | Détourné en Passive Device (voir §2)     |
| Port               | Network Port / Device Port    | Dépend du device parent                  |
| Socket             | Network Port (avec label IN/OUT) | Lié au device, utilisé pour les câbles   |

---

## 2. Détournement ou usage particulier

| Objet modifié      | Adaptation apportée                             |
|--------------------|--------------------------------------------------|
| Room               | Dupliquée en Passive Device avec ports IN/OUT   |
| Hub Ethernet       | Port de plus grand numéro = OUT, les autres = IN|
| Passive Devices    | Standardisés pour tous les éléments à ports pairs|

---

## 3. Nomenclature requise pour cohérence

| Type d'objet       | Format obligatoire                              |
|--------------------|--------------------------------------------------|
| Walloutlet         | `WO <nom de la salle> port n IN/OUT`            |
| Patch Panel        | `PP <nom> port n IN/OUT`                        |
| Switch             | `SW <nom> port n`                               |
| Hub Ethernet       | `HB <nom> port n` (plus grand n = OUT)          |
| Cable              | `C-<nom du device> port n IN/OUT`               |

---

## 4. Contraintes à respecter

- Tous les passive devices doivent avoir un nombre pair de ports.
- Chaque port IN a un port OUT correspondant.
- Tous les noms doivent suivre la nomenclature pour permettre l’interprétation automatique.
- Toutes les connexions doivent être définies dans GLPI via les liens de câbles ou d’associations de ports.

