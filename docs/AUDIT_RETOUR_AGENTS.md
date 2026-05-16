# Audit et Directives de Correction - Retour Principal Engineer

**Date :** 16 Mai 2026  
**Objet :** Rapport de retour critique suite à l'audit technique du projet ImmoGab.  
**Statut :** PRIORITÉ HAUTE - Blocage de la mise en production.

Ce document consigne les manquements critiques identifiés lors de la revue d'architecture et de code. Les agents assignés doivent impérativement traiter ces points avant la prochaine itération de sprint. Le respect de l'architecture hexagonale et des standards de sécurité gabonais (ANINF) n'est pas négociable.

---

## 1. Points de Blocage Critiques (Global)

### Modèles de Données (Infrastructure & Domaine)
- [ ] **Persistance des Transactions :** L'application `payments` utilise des services de transaction sans support de persistance. Le modèle `PaymentTransaction` est absent.
- [ ] **Géolocalisation :** Le modèle `Property` ne contient aucune donnée spatiale. L'ajout de `latitude` et `longitude` est requis pour la conformité aux directives de recherche géographique.

### Backend API (Application Layer)
- [ ] **Exposition du Catalogue :** Les endpoints liés à `Properties` sont inexistants. Le fichier `views.py` est vide et aucune route n'est configurée dans `urls.py`.
- [ ] **Filtrage Métier :** Absence totale de capacités de filtrage par `province` et `type` de bien sur les endpoints de recherche.

### DevOps & Infrastructure
- [ ] **Optimisation Image :** Le `Dockerfile` actuel est monolithique. Une approche **multi-stage build** est exigée pour réduire la surface d'attaque et le poids de l'image de production.

### Sécurité & Conformité
- [ ] **Audit ANINF :** Absence du script automatisé de génération de la nomenclature logicielle sécurisée (SecBOM).

---

## 2. Instructions Spécifiques par Agent

### @Agent-ModelMaker
*Responsabilité : Intégrité et cohérence du Domaine.*
- [ ] **Modèles de Paiement :** Créer l'entité `PaymentTransaction` dans `payments/models.py` incluant `transaction_id`, `amount`, `currency`, `status` (Enum), `provider_reference`, et `timestamp`.
- [ ] **Localisation :** Étendre le modèle `Property` avec les champs `latitude` (DecimalField) et `longitude` (DecimalField).
- [ ] **Arbitrage User :** Résoudre le conflit de définition du modèle User entre les applications `users` et `core`. Le modèle final doit résider dans `users` conformément au standard Django.

### @Agent-Backend
*Responsabilité : Logique applicative et interfaces API.*
- [ ] **Endpoints Properties :** Implémenter le `PropertyViewSet` complet (CRUD) et l'enregistrer dans le routeur de `properties/urls.py`.
- [ ] **Système de Filtres :** Intégrer `django-filter` pour permettre la recherche précise par province, type de bien et plage de prix.
- [ ] **Documentation :** S'assurer que chaque endpoint est documenté via Swagger/OpenAPI.

### @Agent-DevOps
*Responsabilité : Cycle de vie et déploiement.*
- [ ] **Dockerfile Multi-stage :** Refactoriser le `Dockerfile` pour séparer les étapes de construction (build) et d'exécution (runtime). Utiliser des images de base légères (Alpine ou Slim).
- [ ] **Runtime :** S'assurer que les dépendances de développement ne sont pas incluses dans l'image finale.

### @Agent-Security
*Responsabilité : Durcissement et conformité réglementaire.*
- [ ] **SecBOM :** Développer le script `generate_secbom.sh` à la racine du projet. Ce script doit extraire les dépendances (Python & JS) et générer un rapport au format compatible avec les exigences de l'ANINF (ex: CycloneDX ou format JSON structuré).

---

**Validation :** Chaque case cochée devra correspondre à un commit vérifié par les tests d'intégration. Aucune exception ne sera tolérée.

*Signature : Principal Engineer - ImmoGab*
