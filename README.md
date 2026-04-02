# 🐟 Bignon AquaStock

Système complet de gestion pour poissonnerie.

## Stack technique
- Python 3.11
- Django 4.2 LTS
- SQLite (local)
- PyWebView (fenêtre desktop)
- Bootstrap 5 + Bootstrap Icons

## Installation

### 1. Cloner le projet
git clone ...
cd BignonAquaStock
### 2. Créer l'environnement virtuel
python -m venv venv
venv\Scripts\activate
### 3. Installer les dépendances
pip install -r requirements.txt
### 4. Initialiser la base
python manage.py migrate
python manage.py loaddata accounts/fixtures/initial_data.json
### 5. Lancer l'application
python app.py
## Connexion par défaut
- Identifiant : admin
- Mot de passe : admin123

## Compiler en .exe
compiler.bat
## Phases du projet
- ✅ Phase 1 : Application Desktop
- ⬜ Phase 2 : Serveur central API
- ⬜ Phase 3 : Synchronisation
- ⬜ Phase 4 : Dashboard mobile patron
- ⬜ Phase 5 : Site web public