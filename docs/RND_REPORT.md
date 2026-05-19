# Rapport de Recherche et Développement (R&D) - ImmoGab

## 1. Audit de la Pile Technique Actuelle & Sécurité

### État des Lieux
- **Backend :** Django 6.0 + Django REST Framework. Choix optimal pour la sécurité et la conformité KYC.
- **Base de Données :** PostgreSQL 15 (Alpine). Indispensable pour la production et le support de PostGIS pour la géolocalisation.
- **Infrastructure :** Conteneurisation Docker complète avec orchestration via Docker Compose.
- **IoT :** Intégration Jeedom (JSON-RPC) avec stratégie de retry robuste (3 tentatives, backoff exponentiel).

### Évaluation de la Sécurité (Conformité ANINF & Loi 025/2021)
- **Hardening :** Paramètres `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE` et HSTS activés en production.
- **Identité :** Authentification JWT avec rotation de tokens et blacklistage activés.
- **Données :** Localisation systématique des labels via `gettext_lazy` pour garantir l'adhérence aux standards locaux.

---

## 2. Analyse des Coûts d'Infrastructure (Optimisation Budgétaire)

L'objectif est de maintenir un coût opérationnel minimal sans sacrifier la performance.

| Poste | Solution Recommandée | Coût Estime (Mensuel) | Avantages |
| :--- | :--- | :--- | :--- |
| **Serveur (VPS)** | Hetzner Cloud (CX22) / DigitalOcean | ~5 € - 7 € | Performance/prix imbattable. |
| **Base de Données** | PostgreSQL (Auto-hébergé sur Docker) | 0 € | Pas de frais de service managé. |
| **Stockage Médias** | Cloudflare R2 / Backblaze B2 | 0 € - 2 € | Gratuit jusqu'à 10 Go (R2), idéal pour photos. |
| **Cartographie** | Leaflet + OpenStreetMap (OSM) | 0 € | Alternative gratuite à Google Maps API ($200+). |
| **Monitoring** | PostHog (Tier Gratuit) | 0 € | Jusqu'à 100k événements/mois gratuits. |
| **SMS/OTP** | Twilio ou local (Airtel/Moov) | Usage (~0.05€/SMS) | Uniquement pour validation critique. |
| **Total Estimé** | | **~5 € - 10 € / mois** | **Maîtrise totale des coûts.** |

---

## 3. Recommandations d'Innovation & Nouvelles Fonctionnalités

### A. Géolocalisation Avancée (PostGIS + Leaflet)
- **Innovation :** Abandonner l'idée de Google Maps pour passer à **Leaflet.js** avec des tuiles **OpenStreetMap** (ou MapLibre).
- **Technique :** Activer l'extension **PostGIS** sur PostgreSQL pour permettre des recherches de proximité ("Trouver un bien à moins de 2km de moi") ultra-performantes côté serveur.

### B. Automatisation KYC par OCR (Tesseract)
- **Fonctionnalité :** Intégration de `pytesseract` pour l'extraction automatique des données de la CNI gabonaise.
- **Bénéfice :** Réduction du taux d'erreur de saisie manuelle et accélération du processus d'approbation des comptes.
- **Coût :** 0 € (Open-source).

### C. IA d'Estimation des Prix (Machine Learning)
- **Fonctionnalité :** Utiliser `scikit-learn` pour analyser les tendances de prix à Libreville/Port-Gentil et proposer un prix "juste" aux hôtes lors de l'ajout d'un bien.

### D. IoT : Monitoring du Bruit (Anti-Tapage)
- **Innovation :** Utilisation des capteurs de bruit Zigbee/Z-Wave via Jeedom.
- **Logique :** Si le seuil (ex: 80dB) est dépassé pendant plus de 10 min, une alerte est envoyée au dashboard ImmoGab et la caution est automatiquement "gelée" via le module `escrow`.

---

## 4. Propositions d'Optimisation Immédiates

1. **Gestion des Images :** Installer `django-imagekit` pour générer des versions optimisées (WebP) des photos de propriétés afin de réduire le poids des pages de 60%.
2. **Caching de Recherche :** Utiliser Redis pour mettre en cache les résultats de recherche fréquents (ex: "Appartements à Akanda").
3. **Frontend :** Implémenter une **PWA (Progressive Web App)** pour permettre aux utilisateurs gabonais de consulter les biens hors-ligne en cas de micro-coupures réseau.

---
*Rapport rédigé par Jules, Directeur R&D ImmoGab.*
