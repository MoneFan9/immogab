Voici le contenu complet du fichier README.md structuré pour être le cahier des charges principal de votre équipe d'agents. Vous pouvez le copier-coller directement à la racine de votre dépôt GitHub.

Projet ImmoGab - Plateforme Immobilière Hybride au Gabon
1. Vision Stratégique
Imogab est une plateforme proptech destinée au marché gabonais, centralisant l'achat, la vente, et la location longue ou courte durée de biens immobiliers. Sa fonctionnalité différenciatrice est la location de propriétés (maisons, jardins, terrains) à l'heure pour des événements spécifiques (réunions, fêtes, tournages).

2. Stack Technologique Obligatoire
Backend : Python Django & Django REST Framework (DRF).

Conteneurisation : Docker et Docker Compose (utilisation strictement obligatoire pour tous les services afin de garantir la parité entre le développement et la production).

Base de données : PostgreSQL.

3. Architecture des Paiements (Stratégie Modulaire)
Le système ne possède pas encore les clés API de production pour les opérateurs locaux.

Directive de conception : Implémenter le Design Pattern "Strategy". Développer une interface abstraite PaymentGateway.

Implémentation initiale : Créer une classe MockPaymentGateway fonctionnelle qui valide automatiquement toute transaction (simulation d'OTP et de webhook). L'objectif est de pouvoir tester le tunnel de réservation de bout en bout.

Évolutivité : Le système doit être prêt à intégrer les API d'Airtel Money, Moov Money ou d'agrégateurs comme SingPay (qui gère la répartition des fonds isTransfer = true ) par le simple ajout d'une nouvelle classe héritant de l'interface de base, sans modifier la logique métier.  

4. Modélisation de la Base de Données (Django ORM)
Users : Doit inclure un système KYC (Know Your Customer) avec obligation de vérification de pièce d'identité pour se conformer à la Loi 025/2021 sur les transactions électroniques en République Gabonaise.  

Properties : Types : Terrain, Maison, Appartement, Espace Événementiel. Doit inclure la géolocalisation spécifique au Gabon (Province de l'Estuaire, Haut-Ogooué, etc.).

Bookings : Doit gérer une tarification à la micro-durée (start_time et end_time formatés en ISO 8601).

Escrow/Caution : Un modèle spécifique pour bloquer informatiquement une caution liée aux risques de tapage nocturne, la législation prévoyant jusqu'à 1 000 000 FCFA d'amende et des peines de prison pour les troubles de voisinage.  

5. Paramètres de Sécurité (DevSecOps)
Authentification : Implémentation stricte de JWT (JSON Web Tokens) avec un délai d'expiration très court pour limiter les risques de compromission.

Configuration Production : La variable DEBUG = False est obligatoire. Toutes les clés secrètes (SECRET_KEY, identifiants de base de données, etc.) doivent être impérativement isolées dans des variables d'environnement (.env) qui ne seront jamais poussées sur le dépôt.

Conformité Nationale : Le code doit être structuré de manière claire pour permettre un inventaire facile de ses composants logiciels (Software Bill of Materials), se conformant ainsi à la démarche SecBOM impulsée par l'ANINF au Gabon pour la protection des actifs numériques sensibles.

6. Intégration IoT (Domotique Jeedom)
Le point de friction logistique de la location horaire est géré par la domotique. Les réservations confirmées déclencheront des tâches asynchrones envoyant des requêtes webhooks vers l'API HTTP des box Jeedom locales des propriétaires. L'application devra pouvoir modifier l'état de serrures connectées compatibles (comme les modèles Z-Wave PolyLock  ou Nuki ) en accordant un accès temporaire au locataire pendant la durée exacte de son événement.  

7. Coordination de l'Équipe IA
Attention à tous les agents : Vous devez impérativement consulter le fichier AGENTS.md situé à la racine de ce projet avant de générer le moindre plan. Ce fichier définit vos rôles stricts (DevOps, Backend, Sécurité, etc.) et les limites de vos interventions. Ne modifiez jamais les fichiers appartenant au périmètre d'un autre agent.
