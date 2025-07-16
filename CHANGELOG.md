## [MISSION 13.6] - Implémentation du Chargement 'Riche' du Cache via `get_item_details`

- Réécriture complète des méthodes `_load_*` dans `TopologyCache`.
- Le chargement se fait maintenant en deux temps : récupération de la liste des ID, puis appel à `get_item_details` pour chaque objet individuel.
- Cette approche garantit que tous les objets dans le cache sont complets et contiennent tous les attributs nécessaires (comme `_networkports`), résolvant le bug de `get` et préparant `trace`.
- Cette méthode a été validée par nos diagnostics comme étant la seule approche fiable.