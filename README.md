# Challenge Triple A – Dashboard de Monitoring

## Description

Ce projet a pour objectif de développer un outil simple et autonome de monitoring pour une machine virtuelle Linux.  
Le système collecte des informations en temps réel via un script Python et génère une page web statique affichant les statistiques de la machine.

Le projet combine trois compétences principales :
- Administration Linux  
- Algorithmique Python  
- Affichage HTML/CSS  

---

## Prérequis

### Système
- Ubuntu Desktop 22.04 LTS ou plus récent  
- 2 Go RAM minimum  
- 15 Go de stockage  
- Accès internet

### Logiciels
- Python 3.x  
- Module Python : `psutil`

Installation de psutil :

```bash
sudo apt update
sudo apt install python3-pip -y
pip3 install psutil
