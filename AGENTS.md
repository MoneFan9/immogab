# AGENTS.md - Manuel d'Orchestration ImmoGab

## 1. Environnement et Contraintes (Google Jules)

Notre environnement de développement est soumis à des limites d'exécution : un maximum de 15 tâches quotidiennes et 3 exécutions simultanées. Pour orchestrer ce flux de travail asynchrone et éviter les conflits de fusion (merge conflicts), les règles suivantes sont absolues :

* **Isolation :** Chaque agent opère sur une branche Git isolée.
* **Périmètre :** Un agent ne doit en aucun cas modifier le code d'un domaine qui n'est pas formellement assigné à sa spécialité.

## 2. Rôles, Spécialisations et Planification (23 Agents)

### Les Gardiens et Superviseurs (Exécution Quotidienne - 5 tâches/jour)

* **@Agent-QA (2 agents) - 05h00 & 05h30 :** Responsables des tests unitaires et d'intégration via Pytest. Ils simulent les parcours utilisateurs et les erreurs de webhooks.
* **@Agent-Security (1 agent) - 06h00 :** Expert DevSecOps. Audite le code pour prévenir les failles, s'assure que les variables sont masquées, configure les tokens JWT avec expiration courte, et garantit la conformité avec le SecBOM de l'ANINF.
* **@Agent-LeadTech (1 agent) - 07h00 :** Revoit les Pull Requests (PR), vérifie l'architecture globale et l'isolation des composants.
* **@Agent-Validator (1 agent) - 07h30 :** Filet de sécurité final. Repasse sur les PRs approuvées par le Lead Tech pour s'assurer qu'aucun détail n'a été omis avant l'approbation humaine finale.

### Escouade Backend & Data (Lundis, Mercredis, Vendredis - 9 tâches/jour)

* **@Agent-DevOps (1 agent) - 08h00 :** Gère exclusivement l'infrastructure Docker (`Dockerfile`, `docker-compose.yml`) et les dépendances.
* **@Agent-ModelMaker (3 agents) - 08h30, 09h00, 09h30 :** Experts PostgreSQL. Ils créent et maintiennent les fichiers `models.py` (Utilisateurs, Propriétés, Réservations, Cautions) et les migrations.
* **@Agent-Backend (5 agents) - 10h00 à 12h00 (espacés de 30m) :** Ingénieurs API. Ils construisent la logique métier, les vues et les sérialiseurs via Django REST Framework en consommant les modèles existants.

### Escouade Frontend, Intégrations & Innovation (Mardis, Jeudis, Samedis - 8 tâches/jour)

* **@Agent-RnD (1 agent) - 08h00 :** Chercheur. Il scrute les outils open-source, évalue la performance de l'architecture, et propose des optimisations sous forme de rapports Markdown.
* **@Agent-PaymentMock (1 agent) - 08h30 :** Développe l'architecture modulaire `PaymentGateway` et le mock asynchrone des paiements Mobile Money.
* **@Agent-Jeedom (2 agents) - 09h00 & 09h30 :** Ingénieurs IoT. Ils développent les requêtes HTTP POST pour communiquer avec l'API JSON RPC de Jeedom afin d'actionner les serrures connectées.
* **@Agent-Frontend (4 agents) - 10h00 à 11h30 (espacés de 30m) :** Développeurs UI/UX. Ils intègrent les maquettes, les formulaires de réservation et le tableau de bord sans jamais altérer le backend.

### Agent Spécial d'Amorçage

* **@Agent-Init (1 agent) - À la demande (1 seule fois) :** Génère l'arborescence initiale de l'application Django (`django-admin startproject`) et configure les dossiers de base avant de laisser la place aux autres escouades.

## 3. Commandes de l'Espace de Travail

Les agents doivent utiliser les commandes suivantes pour configurer et tester l'environnement local :

* Lancer les conteneurs : `docker-compose up -d`
* Appliquer les migrations : `docker-compose exec web python manage.py migrate`
* Exécuter les tests : `docker-compose exec web pytest`
