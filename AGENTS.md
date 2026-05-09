# AGENTS.md - Manuel d'Orchestration ImmoGab

## 1. Contraintes de l'Environnement et Règles de Base

Notre environnement de développement est soumis à des limites strictes d'exécution : un maximum de 15 tâches quotidiennes et 3 exécutions simultanées. Pour orchestrer le flux de travail et éviter les écrasements de code (merge conflicts), des règles absolues s'appliquent à tous les agents :

* **Isolation :** Chaque agent doit opérer sur une branche Git isolée et se référer exclusivement aux sous-tâches documentées pour sa session.


* **Périmètre :** Un agent ne doit en aucun cas modifier le code d'un domaine ou d'un fichier qui n'est pas formellement assigné à sa spécialité.



## 2. Rôles et Spécialisations de l'Équipe (20 Agents)

### Escouade 1 : DevOps, Sécurité & Modélisation (Fondations)

* **@Agent-DevOps (1 agent) :** Responsable exclusif de l'infrastructure Docker. Cet agent gère uniquement la conteneurisation via les fichiers `Dockerfile`, `docker-compose.yml` et la gestion des paquets dans `requirements.txt`.
* **@Agent-Security (1 agent) :** Responsable DevSecOps. Son rôle est de configurer les middlewares de sécurité Django (CSRF, CORS, protection des endpoints), de s'assurer que `DEBUG=False` est strictement appliqué, de sécuriser l'authentification JWT (avec des délais d'expiration courts) et d'isoler les variables sensibles. Il audite également le code des autres agents pour prévenir les vulnérabilités.
* **@Agent-ModelMaker (2 agents) :** Experts de la donnée. Ils ont l'exclusivité sur la création et la modification des fichiers `models.py` (schémas de base de données) et la génération des scripts de migration PostgreSQL.

### Escouade 2 : Backend & API DRF (Logique Métier)

* **@Agent-Backend (4 agents) :** Architectes du serveur. Ils construisent les vues (`views.py`), les sérialiseurs (`serializers.py`) et le routage d'URL via Django REST Framework, en se basant sur les modèles créés par l'Escouade 1.
* **@Agent-PaymentMock (2 agents) :** Spécialistes des flux financiers. Ils développent l'architecture modulaire via le Design Pattern de Stratégie et mettent en place la passerelle de paiement factice (`MockPaymentGateway`) pour simuler les transactions Mobile Money en attendant les clés API de production.

### Escouade 3 : Intégrations & Domotique

* **@Agent-Jeedom (2 agents) :** Ingénieurs IoT. Ils sont dédiés au développement des requêtes HTTP et des webhooks permettant au backend Django de communiquer avec les box Jeedom locales des propriétaires, afin d'actionner les serrures connectées lors des locations événementielles horaires.



### Escouade 4 : Frontend & Assurance Qualité

* **@Agent-Frontend (5 agents) :** Développeurs UI/UX. Ils créent les interfaces visuelles et les templates, et consomment l'API REST sans jamais altérer la structure ou la logique du serveur backend.


* **@Agent-QA (2 agents) :** Responsables de la fiabilité. Ils rédigent les tests unitaires et d'intégration via Pytest pour valider l'intégrité des flux de réservation, des contraintes KYC et du système de paiement.
* **@Agent-LeadReviewer (1 agent) :** Superviseur final. Il a pour mandat exclusif de relire le code de chaque Pull Request, de s'assurer de la validation sécuritaire par l'Agent-Security, et d'approuver les fusions vers la branche principale.

## 3. Commandes de l'Espace de Travail

Les agents doivent utiliser les commandes suivantes pour configurer et tester l'environnement de manière autonome :

* Lancer les conteneurs : `docker-compose up -d`
* Appliquer les migrations de base de données : `docker-compose exec web python manage.py migrate`
* Exécuter la suite de tests unitaires : `docker-compose exec web pytest`
