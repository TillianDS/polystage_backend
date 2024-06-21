# Polystage Backend

Ce projet est l'API backend de Polystage, une application Django. Ce guide explique comment configurer l'environnement de développement pour ce projet sur Windows et Unix (Linux/macOS). Ainsi que les commandes relatives à la gestion du serveur Django.

Pour toute précision sur Django vous pouvez vous référer à la documentation : https://docs.djangoproject.com/en/5.0/ 

## Configuration de l'environnement de développement

### Prérequis

- Python 3.6 ou supérieur

- pip (Python package installer)

- le clone du projet github


```bash
git clone https://github.com/TillianDS/polystage_backend.git
```

### Instructions

1. Ouvrez l'invite de commande.

2. Naviguez vers le répertoire de votre projet.
3. Exécutez le script de configuration :

#### Windows
   ```bash
   init_env_windows.bat
   ```
#### Unix
   rendre le script exécutabe 
   ```bash
   chmod +x init_env_unix.sh
   ```

   Exécutez le script d'initialisation pour Unix
   ```bash
   ./init_env_unix.sh
   ```

## Lancer le projet Django
se rendre dans le projet polystage_backend contenant le fichier manage.py

   ```bash
   python3 manage.py runserver
   ```

## Dépendances

Les principales dépendances pour ce projet sont :

- Django
- Django REST framework
- django-cas-ng
- django-cors-headers
- django-rest-auth

Toutes les dépendances sont listées dans le fichier `requirements.txt`. Si vous avez besoin d'installer manuellement une dépendance, utilisez la commande suivante :

   ```bash
   pip install nom-de-la-dependance
   ```

N'oubliez pas de mettre à jour `requirements.txt` après l'installation d'une nouvelle dépendance :

   ```bash
   pip freeze > requirements.txt
   ```

## Gestion des fichiers `.gitignore`

Le fichier `.gitignore` est configuré pour exclure les environnements virtuels et les fichiers temporaires.

## Contributions

Les contributions sont les bienvenues ! Veuillez soumettre une pull request pour toute modification ou amélioration.