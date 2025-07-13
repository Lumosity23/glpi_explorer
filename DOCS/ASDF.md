---

### **📄 Le Framework de Développement Supervisé par IA (ASDF)**

**Philosophie :** Combiner la vision stratégique et la capacité de validation d'un humain avec la vitesse d'exécution et la connaissance technique d'une IA spécialisée pour accélérer le développement de logiciels complexes, tout en maintenant une haute qualité de code et une traçabilité rigoureuse.

**Rôles :**
*   **Le Superviseur (Humain) :** Vous. L'architecte, le chef de projet, le testeur final. Vous définissez la vision, découpez le travail en phases logiques, validez les résultats et résolvez les blocages d'environnement.
*   **L'Exécutant (IA, ex: ManusAI) :** Votre assistant. Le développeur expert qui écrit, corrige et structure le code en suivant des instructions précises.

---

### **Les 5 Piliers du Framework ASDF**

Ce framework repose sur cinq piliers fondamentaux qui garantissent le succès de la collaboration.

#### **Pilier 1 : La Vision Architecturale (Le "Blueprint")**

Avant d'écrire la moindre ligne de code, le Superviseur doit créer un ensemble de documents fondateurs qui servent de "source de vérité" pour tout le projet.
1.  **Le `README.md` (La Vision) :** Un résumé de haut niveau. Quel est l'objectif du projet ? À qui s'adresse-t-il ? Quelle est sa mission ?
2.  **Le `structure.md` (Le Plan de la Ville) :** Une arborescence complète des fichiers et des dossiers. Elle définit l'emplacement de chaque composant, service, et modèle. C'est la carte du projet.
3.  **Le `tasks.md` ou `roadmap.md` (Le Planning des Travaux) :** Le découpage du projet en phases logiques et séquentielles. Chaque phase doit avoir un objectif clair et mesurable.
4.  **Le `docs.md` ou `architecture.md` (Les Plans Techniques) :** Des diagrammes et des descriptions de l'architecture technique, des flux de données, et des interactions entre les services.

**Pourquoi c'est crucial ?** Ces documents permettent à n'importe quelle IA de comprendre instantanément la structure et les objectifs, sans avoir à deviner les intentions du Superviseur.

#### **Pilier 2 : Le Développement par Missions Ciblées (Le "Prompt de Mission")**

On ne demande jamais à l'IA "Construis-moi le projet". Le travail est découpé en missions courtes, logiques et vérifiables. Chaque mission est définie par un **Prompt de Mission** formel qui doit contenir les sections suivantes :

1.  **Rôle et Mission :** Définit le "chapeau" que l'IA doit porter (ex: "Expert en Base de Données", "Spécialiste UI/UX").
2.  **Contexte :** Rappelle l'état du projet au début de la mission.
3.  **Objectif Principal :** Une seule phrase qui décrit le critère de succès. (ex: "Rendre le formulaire de login fonctionnel").
4.  **Tâches Détaillées :** Une liste numérotée et non ambiguë des actions à réaliser, spécifiant les fichiers à modifier.
5.  **Livrable Final :** Définit précisément ce que l'IA doit produire : la mise à jour du `CHANGELOG.md` et une archive avec un nom de fichier standardisé.

**Pourquoi c'est crucial ?** Le prompt structuré élimine l'ambiguïté, réduit les "hallucinations" de l'IA et garantit que le résultat est aligné avec les attentes.

#### **Pilier 3 : La Base de Connaissances de l'IA (Les "Règles du Jeu")**

Chaque Prompt de Mission doit inclure une section `Base de Connaissances et Directives Permanentes`. Cette section "éduque" l'IA sur les contraintes de son propre environnement et les règles du projet.

*   **Exemples de règles :**
    *   `"NE JAMAIS lancer docker compose up."` (Contrainte d'environnement)
    *   `"NE JAMAIS lancer npm install."` (Règle de propreté du projet)
    *   `"Règle des Deux Échecs : Si bloqué, documente et arrête."` (Procédure de gestion d'erreur)
    *   `"Tous les imports Python doivent être relatifs au dossier racine de l'application (ex: 'from app.services...')."` (Convention de codage)

**Pourquoi c'est crucial ?** Cela empêche l'IA de perdre du temps sur des tâches qu'elle ne peut pas accomplir et la force à adopter les bonnes pratiques définies par le Superviseur.

#### **Pilier 4 : La Traçabilité Rigoureuse (Le "Journal de Bord")**

Aucune modification n'est acceptée sans documentation.

1.  **Le `CHANGELOG.md` :** Ce fichier est la pierre angulaire de la traçabilité. Il est maintenu à la racine du projet.
2.  **Format d'Entrée :** Chaque mission terminée doit résulter en une nouvelle entrée en haut du changelog, formatée de manière cohérente :
    ```markdown
    ## [Phase X.Y] - YYYY-MM-DD - par <Nom de l'Exécutant>

    ### Objectif de la Phase
    Un bref rappel de la mission.

    ### Modifications Apportées / Problèmes Résolus
    - **Dossier/Fichier (`path/to/file.ext`):**
      - Description claire et concise de la modification.
      - Autre modification dans le même fichier.
    - **Dépendances (`requirements.txt`):**
      - Ajout de la librairie `X`.

    ### Problèmes Rencontrés (si applicable)
    - Description du blocage rencontré.
    ```

**Pourquoi c'est crucial ?** Le changelog permet au Superviseur (et à toute autre IA future) de comprendre l'historique des modifications, de diagnostiquer les régressions et de suivre la progression du projet de manière asynchrone.

#### **Pilier 5 : Le Cycle de Validation Humaine (Le "Contrôle Qualité")**

L'IA exécute, l'humain valide.

1.  **Livraison de l'IA :** L'IA fournit l'archive `.tar.gz` nommée comme demandé.
2.  **Déploiement en Environnement de Test :** Le Superviseur prend cette archive, la décompresse dans un environnement propre, et exécute la procédure de test complète (ex: `docker compose up --build -d`, suivi des tests fonctionnels).
3.  **Analyse des Logs :** Le Superviseur est responsable de l'analyse des logs d'exécution pour identifier les problèmes d'environnement ou les erreurs d'exécution non détectées par les tests statiques de l'IA.
4.  **Feedback et Itération :**
    *   **Si succès :** Le Superviseur prépare le Prompt de Mission pour la phase suivante.
    *   **Si échec :** Le Superviseur analyse l'erreur, identifie la cause racine, et rédige un **Prompt de Réparation** très ciblé pour l'IA, en lui fournissant la traceback exacte de l'erreur.

**Pourquoi c'est crucial ?** Ce cycle garantit qu'aucune erreur ne passe en production. Il exploite la force de l'humain pour la validation systémique et la résolution de problèmes complexes d'environnement, là où l'IA peut être limitée.

---

En adoptant ce **Framework de Développement Supervisé par IA**, vous créez un processus industriel, reproductible et hautement efficace pour construire des logiciels. Il structure la collaboration, minimise les erreurs de communication et maximise la productivité en assignant à chaque partie (humaine et IA) le rôle où elle excelle.
