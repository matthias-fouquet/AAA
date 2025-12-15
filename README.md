# Challenge Triple A – Dashboard de Monitoring Système

## Description du projet

Ce projet consiste à développer un **outil de monitoring système autonome** permettant de surveiller en temps réel les ressources d’une machine Linux.  
Les informations sont collectées via un script Python, puis affichées dans une **page web statique générée automatiquement**.

L’objectif est de démontrer la capacité à :
- collecter des données système
- les traiter côté Python
- les restituer de manière lisible et structurée en HTML/CSS

Aucune base de données ni serveur web n’est utilisé : le système repose uniquement sur Python et des fichiers statiques.

---

## Fonctionnalités

### Informations système
- Nom de la machine
- Modèle
- Numéro de série
- Processeur (CPU)
- Carte graphique (GPU)
- Système d’exploitation (Linux / macOS)
- Version du système
- Heure de démarrage
- Uptime
- Nombre d’utilisateurs connectés

### Monitoring CPU
- Pourcentage global d’utilisation CPU
- Utilisation par cœur
- Fréquence maximale du processeur
- Top processus consommateurs de CPU
- Barre de progression avec code couleur :
  - Vert : 0–50 %
  - Orange : 51–80 %
  - Rouge : 81–100 %

### Monitoring RAM
- Quantité totale de RAM
- RAM disponible
- Architecture mémoire
- RAM par cœur
- Mémoire swap
- Pourcentage d’utilisation RAM
- Top processus consommateurs de mémoire
- Barre de progression avec code couleur :
  - Vert : 0–50 %
  - Orange : 51–80 %
  - Rouge : 81–100 %

### Load Average (charge système)
- Load average sur 1, 5 et 15 minutes
- Conversion en pourcentage par rapport au nombre de cœurs CPU
- Indicateur d’état global :
  - OK
  - HIGH
  - CRITICAL

### Analyse de fichiers
- Analyse récursive d’un répertoire (Documents)
- Analyse de plus de 10 extensions de fichiers
- Nombre de fichiers par extension
- Pourcentage par type de fichier
- Espace disque occupé par extension
- Taille totale du répertoire analysé
- Top 5 des fichiers les plus volumineux

### Réseau
- Adresse IP principale
- Interfaces réseau et adresses IPv4

---

## Architecture du projet

```
AAA/
├── monitor.py        # Script Python de collecte et génération HTML
├── template.html     # Template HTML avec variables dynamiques
├── template.css      # Feuille de style du dashboard
├── index.html        # Page générée automatiquement
└── README.md
```

---

## Prérequis

### Système
- Linux (Ubuntu Desktop 22.04 LTS ou plus récent recommandé)
- 2 Go de RAM minimum
- 15 Go d’espace disque
- Accès internet

### Logiciels
- Python 3.x
- Module Python : `psutil`

Installation de `psutil` :

```bash
sudo apt update
sudo apt install python3-pip -y
pip3 install psutil
```

---

## Installation et utilisation

1. Cloner ou copier le projet sur la machine cible
2. Installer les dépendances
3. Lancer le script Python :

```bash
python3 monitor.py
```

4. Ouvrir le fichier `index.html` dans un navigateur web

Le script :
- régénère automatiquement la page toutes les 30 secondes
- met à jour les statistiques système en temps réel
- peut être arrêté proprement avec `Ctrl + C`

---

## Choix techniques

- **Python + psutil** : accès fiable et multiplateforme aux informations système
- **HTML/CSS statique** : aucune dépendance serveur
- **Templates dynamiques** : séparation claire entre logique et affichage
- **Meta refresh HTML** : rafraîchissement automatique sans JavaScript
- **Code couleur** : lecture immédiate de l’état de la machine

---

## Objectifs pédagogiques

- Administration système Linux
- Collecte et traitement de données système
- Algorithmique Python
- Génération dynamique de contenu HTML
- Structuration et mise en forme CSS
- Compréhension des indicateurs de performance système

---

## Auteur

Projet réalisé dans le cadre du **Challenge Triple A**  
Bachelor IT – 1re année  
La Plateforme_