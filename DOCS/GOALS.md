# Objectif du projet

Développer un outil en ligne de commande (CLI) permettant de retracer n'importe quel équipement réseau (ordinateur, switch, hub Ethernet, patch panel, etc.) présent dans l'infrastructure décrite dans GLPI.

L'outil doit :
- Identifier tous les ports, sockets et câbles connectés à l’équipement.
- Extraire les informations de routage physique et logique via l’API GLPI.
- Localiser chaque device (nom, salle/room, statut).
- Reconstituer la chaîne de connexion jusqu’au routeur ou vers les terminaux associés.
- Fournir une visualisation en texte claire et intuitive de l’ensemble des connexions.

Ce projet utilise les données du parc informatique de GLPI modélisé avec une nomenclature spécifique (voir `NOMENCLATURE.md`).
