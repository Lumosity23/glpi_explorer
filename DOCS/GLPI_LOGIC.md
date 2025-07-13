# LOGIQUE DE GESTION DES CONNEXIONS RÉSEAU DANS GLPI – PC À SWITCH

## 1. Introduction

Ce document décrit la logique précise de gestion des connexions physiques et logiques entre les différents devices réseau dans GLPI, en partant d’un PC jusqu’à un switch. L’objectif est de clarifier la distinction entre les ports physiques (sockets) et les ports logiques (ports Ethernet), et d’établir un chemin réseau cohérent basé sur cette distinction.

---

## 2. Définitions Clés

- **Socket** : Port physique réel sur un device, représentant une connexion matérielle.
- **Port Ethernet** : Port logique, utilisé pour représenter la connexion réseau au niveau logiciel entre devices.

---

## 3. Exemple de Chaîne de Connexion (PC → Switch)

### Étape 1 : PC  
- Le PC possède des ports Ethernet (logiques) et des sockets (physiques).  
- **Important** : Ne pas confondre les ports Ethernet (logiques) avec les sockets (physiques).  
- Le PC se connecte à un hub Ethernet via un câble nommé selon la convention, par exemple :  
  - `C-PC1` reliant un socket du PC à un port/socket IN du hub.

### Étape 2 : Hub Ethernet  
- Le hub a plusieurs ports/sockets IN (pour connecter les devices en amont).  
- Il possède **un seul port/sockets OUT** qui représente la sortie principale du hub vers la suite du réseau.  
- Le câble reliant le port OUT du hub vers l’élément suivant suit la convention :  
  - `C-HB ethernet`

### Étape 3 : Walloutlet  
- Le câble `C-HB ethernet` connecte un port/sockets IN du walloutlet, ce dernier est lié directement à son homologue port OUT (sans câble physique, cette liaison est induite par le programme).  
- Le port OUT du walloutlet se connecte ensuite à un câble vers le patch panel.

### Étape 4 : Patch Panel  
- Le câble reliant le walloutlet OUT au patch panel porte un nom du type :  
  - `C-WO port n`  
- Le patch panel comporte un port frontal (front port) connecté à un port arrière (rear port) du même numéro, différenciés par `IN` et `OUT` dans le nom du port.  
- Le port OUT du patch panel se connecte ensuite au switch.

### Étape 5 : Switch  
- La destination finale dans cet exemple simple est un switch connecté via un port logique identifié, par exemple :  
  - `SW port 0`

---

## 4. Remarques Importantes

- Le chemin réseau peut inclure plusieurs patch panels ou ne pas contenir de hub, selon la configuration réelle.  
- L’essentiel est de respecter la logique derrière chaque device et sa connexion physique ou logique.  
- **Ne jamais confondre les ports Ethernet (logiques) avec les sockets (physiques)**, car cela pourrait fausser la modélisation du réseau.

---

## 5. Schéma Simplifié du Chemin

```plaintext
PC (socket) --C-PC1--> Hub (port IN) --(Hub port OUT)--> C-HB ethernet --> Walloutlet port IN --(induit)--> Walloutlet port OUT --C-WO port n--> Patch Panel front port IN -- Patch Panel rear port OUT --> Switch port 0
