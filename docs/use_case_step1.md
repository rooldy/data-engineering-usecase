# Use Case : Plateforme E-commerce — Description métier

## 1. Contexte
Une entreprise e-commerce souhaite améliorer sa visibilité sur les performances commerciales et opérationnelles afin d’optimiser :
- les décisions marketing (promotions, ciblage),
- la gestion des stocks,
- le parcours client,
- et la prévision de ventes.

Le projet vise à construire un pipeline de données automatisé (ingestion → transformation → consommation) pour fournir des rapports et indicateurs fiables aux équipes métiers.

## 2. Problématique / douleur métier
Actuellement, les équipes rencontrent plusieurs difficultés :
- Données opérationnelles dispersées dans plusieurs systèmes (transactionnel, ERP, logs web).
- Absence d’un entrepôt marchand unifié pour calculer les KPIs quotidiens.
- Latence manuelle dans la production des rapports (procédures manuelles, erreurs humaines).
- Difficulté à mesurer précisément l'impact des promotions et ruptures de stock.

## 3. Objectifs business
Le pipeline vise à atteindre les objectifs suivants :
1. Automatiser la consolidation des données de vente et produit (toutes les 24h).
2. Fournir des KPIs fiables et reproductibles pour le suivi quotidien.
3. Permettre l’analyse de l’impact des promotions et des remises sur le chiffre d’affaires.
4. Détecter rapidement les anomalies de ventes (pic imprévu, forte chute).
5. Mettre à disposition des datasets prêts pour les data scientists (modélisation, prévisions).

## 4. Indicateurs clés de performance (KPIs)
KPI primaires à produire automatiquement :
- **Total Revenue** (CA) — journée / semaine / mois
- **Nombre de commandes** — journée / semaine / mois
- **Average Order Value (AOV)** — moyenne du panier
- **Customer Lifetime Value (CLV)** — par client
- **Top 10 produits par revenue**
- **Revenue par catégorie**
- **Taux de conversion** (si logs web disponibles)
- **Taux de retour / retours par produit**
- **Taux de rupture de stock** (sur période donnée)
- **Impact promotionnel** : delta CA avant / pendant / après promotion

KPIs secondaires (analyses avancées) :
- **Segmentations clients** (RFM, cohortes)
- **Prévision des ventes** (horizon 7 / 30 / 90 jours)
- **Alerting** : détection d’anomalies (seuils configurables)

## 5. Utilisateurs / personas
Les livrables serviront à différents profils au sein de l’entreprise :
- **Data Analyst** : exploration ad-hoc, création de dashboards.
- **Data Scientist** : accès aux données nettoyées pour modélisation (churn, forecast).
- **Responsable Marketing** : analyse d’impact des promotions, segmentation.
- **Supply Chain / Logistique** : suivi des niveaux de stock et alertes rupture.
- **Direction / Finance** : rapports topline (CA, marges).
- **Equipe Produit / Merchandising** : performance produit, pricing.

## 6. Décisions attendues grâce aux données
La plateforme doit permettre de prendre des décisions concrètes :
- Ajustement des promotions (qui, quand, pour quel produit).
- Remontée et priorisation des réapprovisionnements.
- Actions de rétention ciblées pour segments à forte valeur.
- Allocation budgétaire marketing selon ROI produit/catégorie.

## 7. Critères de succès (acceptance criteria)
Le projet sera considéré comme réussi si :
1. Les pipelines s'exécutent automatiquement (cron / Airflow), sans intervention manuelle, et terminent avec un statut "SUCCESS".
2. Les KPIs quotidiens sont disponibles chaque matin (D+1) dans la zone analytics.
3. Les jeux de données (bronze → silver → gold) respectent les règles de qualité définies (pas de nulls sur clés primaires, dates cohérentes, prix ≥ 0).
4. Les dashboards métiers affichent les KPIs et sont validés par l'équipe marketing/finance.
5. Les tests unitaires et d’intégration couvrent les transformations critiques (coverage minimal à définir).

## 8. Contraintes & risques
- **Données sensibles** : respecter la confidentialité des données clients (anonymisation/masquage si nécessaire).
- **Volumétrie** : logs web potentiellement très volumineux → prévoir stockage scalable ou échantillonnage.
- **Latence** : batch quotidien acceptable ; si besoin temps réel, réévaluer architecture.
- **Dépendances externes** : qualité et disponibilité des exports (ERP, plateformes de paiement).

## 9. Étapes successives (aperçu)
1. Définir schéma source et contract des fichiers d’ingestion.
2. Mettre en place la zone `raw` et scripts d’ingestion (Pandas / API).
3. Implémenter transformations PySpark (clean → normalized).
4. Construire agrégations / tables analytiques (gold).
5. Orchestration avec Airflow et monitoring.
6. Exposer outputs : dashboards & API.

