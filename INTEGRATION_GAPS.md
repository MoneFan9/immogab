# Rapport de Rupture de la Chaîne d'Intégration - ImmoGab

En tant qu'Ingénieur Testeur, j'ai analysé le parcours de bout en bout (Recherche -> Paiement -> Jeedom). Bien que la logique métier soit fonctionnelle en simulation, plusieurs ruptures critiques subsistent dans la chaîne d'intégration réelle.

## 1. Ruptures Identifiées

### A. Dépendance aux Mocks dans le Code Source
**Observation :** Le fichier `immogab/services.py` contient des données codées en dur (`mock_properties`) et utilise `unittest.mock.MagicMock` directement dans la logique de recherche.
**Impact :** L'application ne peut pas fonctionner en production sans une base de données réelle. Les tests actuels ne testent pas l'interaction avec l'ORM Django.

### B. Absence de Persistance (PostgreSQL)
**Observation :** Le projet utilise SQLite (`db.sqlite3`) par défaut. Les directives du projet (README et Audit Technique) exigent PostgreSQL 15+.
**Impact :** Risque de divergence de comportement entre le développement et la production (notamment sur la gestion des transactions et des types ENUM).

### C. Manque de Conteneurisation
**Observation :** Aucun `Dockerfile` ou `docker-compose.yml` n'est présent.
**Impact :** Difficulté à garantir la reproductibilité des environnements de test et d'intégration. La chaîne CI/CD est inexistante.

### D. Centralisation Excessive
**Observation :** Toute la logique (KYC, Booking, Search, Payment, IoT) est regroupée dans `immogab/services.py`.
**Impact :** Violation des principes de modularité Django. La maintenance deviendra difficile à mesure que le projet croît. Les applications `core`, `properties` et `payments` doivent être créées.

## 2. Recommandations de Correction

1.  **Migrer vers PostgreSQL :** Configurer les paramètres de base de données dans Django et fournir les fichiers Docker nécessaires.
2.  **Modularisation :** Répartir la logique de `services.py` dans les applications Django respectives.
3.  **Utilisation de l'ORM :** Remplacer les listes de mocks par des requêtes QuerySet réelles dans `search_properties`.
4.  **Tests sur Données Réelles :** Mettre à jour la suite de tests pour utiliser `pytest-django` avec une base de données de test réelle au lieu de mocks de modèles.

---
**Rapport établi le :** 2026-05-15
**Signé :** Jules, Ingénieur Testeur
