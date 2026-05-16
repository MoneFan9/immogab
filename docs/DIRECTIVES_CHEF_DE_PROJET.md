# Directives Techniques - Projet ImmoGab

> [!IMPORTANT]
> **ALERTE AUDIT :** Un audit technique complet a été réalisé le 2026-05-16. 
> Tous les agents (DevOps, ModelMaker, Backend, Security) et le Tech Lead **DOIVENT** consulter le rapport de retour détaillé ici : [docs/AUDIT_RETOUR_AGENTS.md](./AUDIT_RETOUR_AGENTS.md) avant de poursuivre tout travail.

Ce document centralise les instructions du Chef de Projet traduites en spécifications techniques pour les différents agents du projet.

## 1. Priorités Immédiates (Cycle Prochain)

### @Agent-DevOps
*   **Conteneurisation :** Créer un `Dockerfile` multi-étapes pour l'application Django (Python 3.11+).
*   **Orchestration :** Configurer un fichier `docker-compose.yml` incluant :
    *   Le service `web` (Django).
    *   Le service `db` (PostgreSQL 15+).
    *   Un volume persistant pour les données de la base.
*   **Environnement :** Préparer un fichier `.env.example` avec toutes les variables nécessaires (DB_NAME, DB_USER, DB_PASSWORD, SECRET_KEY, DEBUG).

### @Agent-ModelMaker
*   **Application 'core' :** Initialiser une application Django nommée `core` ou `properties`.
*   **Modèles de base :**
    *   `User` : Étendre le modèle User de Django pour inclure les champs KYC (Numéro de pièce d'identité, type de pièce, statut de vérification).
    *   `Property` : Inclure les champs Type (ENUM), Titre, Description, Prix (horaire/journalier), Géolocalisation (Province, Ville, Quartier, Coordonnées GPS).
    *   `Booking` : Gérer les relations User/Property, les dates/heures (ISO 8601) et le statut de la réservation.
    *   `Escrow` : Modèle pour la gestion des cautions liées aux réservations.

## 2. Spécifications Backend & Paiement

### @Agent-PaymentMock
*   **Design Pattern :** Implémenter l'interface abstraite `PaymentGateway` dans un module `payments/interfaces.py`.
*   **Mock :** Créer `MockPaymentGateway` qui simule une validation de transaction réussie après un délai court (simulation asynchrone).

### @Agent-Backend
*   **API REST :** Utiliser Django REST Framework pour créer les endpoints CRUD pour les propriétés et les réservations.
*   **Filtrage :** Implémenter des filtres par province et par type de bien.

## 3. Sécurité & Conformité

### @Agent-Security
*   **Auth :** Configurer `djangorestframework-simplejwt`.
*   **Validation :** S'assurer que `DEBUG` est toujours à `False` en dehors de l'environnement de développement.
*   **Audit :** Préparer le script de génération du SecBOM (Software Bill of Materials) pour l'ANINF.

## 4. Intégration IoT

### @Agent-Jeedom
*   **Architecture :** Préparer un service ou un signal Django qui se déclenche lors de la confirmation d'une réservation pour préparer l'appel au webhook Jeedom.
*   **API :** Étudier l'API JSON RPC de Jeedom pour l'ouverture/fermeture des serrures.

---
*Dernière mise à jour : 2026-05-10*
