# Nomenclature des Devices – Projet GLPI

---

## Règles Générales de Nomenclature

- Les noms des passive devices et network devices suivent ce schéma :  
  - **Hub** → `HB`  
  - **Patch Panel** → `PP`  
  - **Switch** → `SW`  
  - **Walloutlet** → `WO <nom de la room>`

- Les walloutlets incluent le nom complet de la salle dans laquelle ils sont situés.  
- Après le préfixe, le device peut comporter n'importe quel nom utile pour le reconnaître.

---

## Détails par Type de Device

### Passives Devices  
- Chaque passive device doit avoir un nombre pair de ports.  
- Chaque port IN possède un port OUT correspondant.

### Walloutlets  
- Possèdent des ports IN et OUT.  
- Nomenclature :  
  - `WO <nom de la room> port n IN`  
  - `WO <nom de la room> port n OUT`

### Patch Panels  
- Nomenclature :  
  - `PP <nom du patch panel> port n IN`  
  - `PP <nom du patch panel> port n OUT`

### Switches  
- Tous les ports commencent par `SW`.  
- Exemple : `SW <nom du switch> port n`

### Hubs  
- Tous les ports commencent par `HB`.  
- Exemple : `HB <nom du hub> port n`  
- Le port ayant le numéro le plus élevé est défini comme sortie principale (OUT).

### Câbles  
- Identifiés par :  
  - `C-<nom du device A> port n IN/OUT`  
- Si le device a un seul port, la mention du port peut être omise.

---

