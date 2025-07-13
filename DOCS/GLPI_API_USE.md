# GLPI API - Guide d'utilisation pour projet GLPI Explorer

---

## 1. Introduction rapide

L’API REST de GLPI permet d’interagir avec la base de données GLPI sans accès direct à celle-ci. On peut récupérer, modifier, créer ou supprimer des données (ordinateurs, utilisateurs, tickets, etc.) via des requêtes HTTP.  
C’est idéal pour créer un explorateur ou un outil d’administration externe.

---

## 2. Authentification

- **Endpoint :** `/apirest.php/initSession`
- **Méthode :** POST
- **Données :**
  ```json
  {
    "login": "ton_utilisateur",
    "password": "ton_mot_de_passe"
  }
Réponse :
Un session_token que tu dois inclure dans le header Session-Token pour toutes les requêtes suivantes.

3. Headers généraux à inclure dans chaque requête (après authentification)
http
Copy
Edit
Content-Type: application/json
Session-Token: ton_session_token
App-Token: ton_app_token (si configuré dans GLPI)
Le App-Token est optionnel mais recommandé pour plus de sécurité.

4. Principales opérations CRUD sur les objets
a) Récupérer des données (GET)
Exemple: Obtenir la liste des ordinateurs
GET /apirest.php/Computer

Avec filtre (exemple : statut actif):
GET /apirest.php/Computer?criteria[0][field]=status&criteria[0][value]=1

Pagination :
Utilise Range dans le header :
Range: items=0-10 pour les 10 premiers éléments.

b) Créer un objet (POST)
Exemple: Créer un nouvel utilisateur
Endpoint : /apirest.php/User
Données envoyées en JSON :

json
Copy
Edit
{
  "name": "Dupont",
  "realname": "Jean",
  "email": "jean.dupont@example.com"
}
c) Modifier un objet (PUT)
Exemple: Modifier un utilisateur
Endpoint : /apirest.php/User/{id}
Données JSON avec les champs à modifier.

d) Supprimer un objet (DELETE)
Exemple :
DELETE /apirest.php/User/{id}

5. Structure des données
Chaque objet correspond à une table de la base de données GLPI.

Les champs disponibles sont ceux définis dans GLPI (ex: pour Computer : name, serial, contacts_id, etc.).

Tu peux utiliser la requête GET sur /apirest.php/{objet}/schema pour récupérer la structure des données.

6. Exemples concrets
Exemple 1 : Récupérer la liste des tickets ouverts
http
Copy
Edit
GET /apirest.php/Ticket?criteria[0][field]=status&criteria[0][value]=1
Headers:
Session-Token: ton_session_token
Exemple 2 : Créer un ticket
http
Copy
Edit
POST /apirest.php/Ticket
Headers:
Session-Token: ton_session_token
Content-Type: application/json

{
  "name": "Problème imprimante",
  "content": "L’imprimante ne répond plus",
  "status": 1,
  "users_id_recipient": 5
}
7. Sécurité et bonnes pratiques
Utilise toujours HTTPS pour sécuriser les échanges.

Ne partage jamais tes tokens publiquement.

Limite les droits de l’utilisateur API utilisé.

Nettoie tes sessions (closeSession) quand tu as fini.

8. Fermeture de session
Endpoint: /apirest.php/killSession

Méthode: POST

Données:

json
Copy
Edit
{ "session_token": "le_token" }
9. Documentation officielle utile
https://glpi-developer-documentation.readthedocs.io/en/latest/apirest/

https://glpi-installation-guide.readthedocs.io/en/latest/api/

Si tu veux, je peux aussi t’aider à coder des exemples en Python ou autre langage pour interagir avec cette API. Ça te branche ?

bash
Copy
Edit

Tu peux copier-coller ce texte dans un fichier `GLPI_API_Usage.md` et ça sera nickel.  
Dis-moi si tu veux que je te prépare aussi un script Python d’exemple pour tester l’API !