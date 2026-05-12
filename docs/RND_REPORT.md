# Rapport R&D ImmoGab - Innovation et Maîtrise des Coûts

## 1. Analyse des choix techniques actuels

L'audit actuel révèle des écarts critiques entre la vision stratégique et l'implémentation technique :

*   **Base de données :** L'utilisation de SQLite en développement, bien que gratuite, ne respecte pas la parité dev/prod et risque de poser des problèmes de concurrence lors des réservations horaires.
*   **Infrastructure :** L'absence de conteneurisation (Docker) freine le déploiement continu et augmente les risques d'erreurs liées à l'environnement.
*   **Logique métier :** L'usage de `MagicMock` dans `services.py` est une dette technique majeure qui empêche de tester la réalité des interactions avec la base de données.

## 2. Recommandations et Optimisations Open-Source

Pour garantir la scalabilité à moindre coût, nous proposons l'adoption des outils suivants :

*   **PostgreSQL (Mandat) :** Transition immédiate vers PostgreSQL pour la gestion robuste des transactions et des index géospatiaux (PostGIS à envisager pour la géolocalisation précise au Gabon).
*   **Celery & Redis :** Pour la validation asynchrone du KYC et les appels IoT (Jeedom), évitant ainsi de bloquer le thread principal de l'API.
*   **Nginx & Gunicorn :** Stack standard et performante pour servir l'application Django de manière sécurisée.

## 3. Nouvelles Fonctionnalités Innovantes

*   **Estimation de Prix par IA :** Utiliser des modèles de machine learning simples (scikit-learn) pour suggérer un prix de location optimal basé sur la zone géographique et le type de bien.
*   **Application Web Progressive (PWA) :** Permettre une expérience mobile fluide sans les coûts de développement et de maintenance des stores (App Store/Play Store), tout en offrant des notifications push pour les réservations.
*   **Tableau de bord Énergétique IoT :** Intégration avancée avec Jeedom pour permettre aux propriétaires de surveiller la consommation électrique pendant les locations horaires.

## 4. Évaluation du Coût Théorique des Infrastructures

| Composant | Solution Proposée | Coût Mensuel Estimé (Hébergement VPS) | Alternative Cloud (AWS/Azure) |
| :--- | :--- | :--- | :--- |
| Serveur Web/App | VPS Entry Level (2 vCPU, 4GB RAM) | ~5€ - 10€ | ~30€+ (EC2 t3.medium) |
| Base de Données | Auto-hébergée sur VPS | 0€ (inclus) | ~15€+ (RDS) |
| Cache/Queue | Redis (Auto-hébergé) | 0€ (inclus) | ~15€+ (ElastiCache) |
| Stockage KYC | MinIO (Open-source S3) | 0€ (inclus) | Coût au Go (S3) |
| **Total Estimé** | | **~10€ / mois** | **~60€+ / mois** |

*Note : L'auto-hébergement sur un VPS sécurisé offre un contrôle total et une réduction des coûts de 80% par rapport aux services managés pour la phase de lancement.*

## 5. Conclusion

La priorité absolue est la mise en conformité avec la stack Docker/PostgreSQL. L'introduction de Celery/Redis permettra de supporter la montée en charge des interactions IoT et KYC sans surcoût infrastructurel majeur.
