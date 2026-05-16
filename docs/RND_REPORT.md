# Rapport de Recherche et Développement (R&D) - ImmoGab

## 1. Audit de la Pile Technique Actuelle

### État des Lieux
- **Backend :** Django & Django REST Framework (DRF). Choix robuste pour la gestion des données structurées et la conformité KYC.
- **Base de Données :** Actuellement configurée sur SQLite dans certains environnements. **Critique :** Le passage à PostgreSQL est impératif pour la production (gestion des verrous, concurrence, intégrité des données).
- **Conteneurisation :** Docker/Docker Compose. Essentiel pour la reproductibilité.
- **IoT :** Intégration Jeedom via JSON-RPC.

### Évaluation des Alternatives Open-Source
- **Framework :** Django reste la meilleure option "batteries-included" pour une plateforme immobilière complexe. FastAPI pourrait être envisagé pour des microservices haute performance à l'avenir.
- **IoT :** Home Assistant est une alternative à Jeedom, souvent jugée plus moderne et dotée d'une communauté plus vaste. Cependant, Jeedom a une forte implantation locale et une gestion de plugins (PolyLock/Nuki) très stable.

---

## 2. Estimation Théorique des Coûts d'Infrastructure

| Poste | Solution Recommandée | Coût Estime (Mensuel) | Avantages |
| :--- | :--- | :--- | :--- |
| **Hébergement VPS** | DigitalOcean (Droplet) ou Hetzner | 4 € - 10 € | Rapport performance/prix imbattable. |
| **Base de Données** | PostgreSQL (Auto-hébergé sur Docker) | 0 € | Économie par rapport aux instances gérées. |
| **Cache & Tasks** | Redis (Docker) | 0 € | Performance accrue pour les sessions et tâches Celery. |
| **Stockage Médias** | Backblaze B2 ou AWS S3 (S3-compatible) | 1 € - 5 € | Évolutivité pour les photos haute résolution. |
| **Monitoring** | Sentry (Tier Gratuit) / BetterStack | 0 € | Alerting en cas d'erreur. |
| **Total Estimé** | | **~5 € - 15 € / mois** | **Maîtrise absolue des coûts.** |

*Note : Un hébergement local au Gabon (ex: HostZealot) peut coûter plus cher (~15-30€) mais offre une meilleure latence pour les utilisateurs locaux.*

---

## 3. Analyse Paiements & Conformité (Loi 025/2021)

### Paiements Mobile Money
- **Option A : SingPay (Agrégateur)**
  - *Coût :* Commission sur transaction (~2-4%).
  - *Avantage :* Intégration unique pour Airtel Money et Moov Money. Répartition des fonds native (`isTransfer`).
- **Option B : API Directes Opérateurs**
  - *Coût :* Frais de mise en service potentiels, mais commissions réduites.
  - *Inconvénient :* Complexité administrative et technique (double intégration).

### KYC (Know Your Customer)
- **Démarche Actuelle :** Saisie manuelle du numéro de pièce d'identité.
- **Recommandation R&D :** Intégration d'une bibliothèque OCR open-source (Tesseract) pour extraire automatiquement les informations des photos de cartes d'identité. Cela réduit la friction utilisateur et limite les erreurs de saisie tout en respectant la Loi 025/2021 sur la protection des données.

---

## 4. Recommandations d'Optimisation & Innovation

### Optimisations Immédiates
1. **Caching :** Implémenter `django-redis` pour mettre en cache les recherches de propriétés fréquentes.
2. **PgBouncer :** Utiliser PgBouncer pour gérer efficacement le pool de connexions PostgreSQL dans Docker.
3. **Optimisation d'Images :** Utiliser `django-imagekit` pour générer des miniatures automatiquement et réduire la bande passante consommée.

### Roadmap Innovation
- **Estimation de Prix par IA :** Utiliser une bibliothèque comme `scikit-learn` pour proposer une estimation automatique du prix de location en fonction du quartier, du type de bien et des équipements.
- **Application Web Progressive (PWA) :** Transformer le frontend en PWA pour permettre un accès fluide même avec une connexion internet instable au Gabon.
- **Extension IoT :** Intégration de capteurs de bruit connectés à Jeedom pour alerter automatiquement le propriétaire et l'équipe ImmoGab en cas de dépassement des seuils de décibels (Anti-tapage nocturne), protégeant ainsi la caution.

---
*Rapport rédigé par Jules, Directeur R&D ImmoGab.*
