## [MISSION 13.7] - Correction du Parsing des Données de Ports

- La logique d'affichage de la commande 'get' a été corrigée pour gérer la structure de dictionnaire de la clé `_networkports`.
- Le code parcourt maintenant correctement les différents types de ports (Ethernet, Wifi, etc.) et les affiche dans la table.
- Cette correction résout le bug où les détails des ports n'apparaissaient pas pour un équipement.