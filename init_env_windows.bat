@echo off
REM Créer un environnement virtuel nommé .venv
python -m venv .venv

REM Activer l'environnement virtuel
call .\.venv\Scripts\activate

REM Mettre à jour pip
python -m pip install --upgrade pip

REM Installer les dépendances à partir de requirements.txt
if exist requirements.txt (
    pip install -r requirements.txt
) else (
    echo "Le fichier requirements.txt n'a pas été trouvé."
)

echo "Environnement virtuel initialisé et dépendances installées."
