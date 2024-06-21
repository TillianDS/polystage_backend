#!/bin/bash

# Créer un environnement virtuel nommé .venv
python3 -m venv .venv

# Activer l'environnement virtuel
source .venv/bin/activate

# Mettre à jour pip
pip install --upgrade pip

# Installer les dépendances à partir de requirements.txt
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    echo "Le fichier requirements.txt n'a pas été trouvé."
fi

echo "Environnement virtuel initialisé et dépendances installées."
