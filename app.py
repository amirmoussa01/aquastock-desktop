import sys
import os
import threading
import time
import webview

# ─────────────────────────────────────
# Configuration des chemins
# ─────────────────────────────────────
if getattr(sys, 'frozen', False):
    # Mode .exe compilé
    BASE_DIR = os.path.dirname(sys.executable)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
    # Ajouter le dossier _internal au path
    INTERNAL_DIR = os.path.join(BASE_DIR, '_internal')
    if INTERNAL_DIR not in sys.path:
        sys.path.insert(0, INTERNAL_DIR)
else:
    # Mode développement
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
    if BASE_DIR not in sys.path:
        sys.path.insert(0, BASE_DIR)

import django
django.setup()


def initialiser_base():
    """Crée les tables et charge les données initiales"""
    from django.core.management import call_command
    from accounts.models import Utilisateur

    call_command('migrate', '--run-syncdb', verbosity=0)

    if not Utilisateur.objects.exists():
        if getattr(sys, 'frozen', False):
            fixture_path = os.path.join(
                BASE_DIR, '_internal',
                'accounts', 'fixtures', 'initial_data.json'
            )
        else:
            fixture_path = os.path.join(
                BASE_DIR, 'accounts', 'fixtures', 'initial_data.json'
            )

        if os.path.exists(fixture_path):
            call_command('loaddata', fixture_path, verbosity=0)
        else:
            Utilisateur.objects.create_superuser(
                username='admin',
                password='admin123',
                first_name='Administrateur',
                last_name='AquaStock',
                role='admin',
                est_actif=True,
            )
        print("Base initialisée.")


def synchronisation_periodique():
    """Lance la sync toutes les X minutes"""
    from django.conf import settings
    interval = getattr(settings, 'SYNC_INTERVAL', 300)
    time.sleep(30)

    while True:
        try:
            from sync.service import synchroniser
            resultat = synchroniser()
            print(f"Sync : {resultat.get('statut')} – {resultat.get('message')}")
        except Exception as e:
            print(f"Erreur sync : {e}")
        time.sleep(interval)


def demarrer_django():
    """Démarre le serveur Django en arrière-plan"""
    from django.core.management import call_command

    # Changer le dossier courant selon contexte
    if getattr(sys, 'frozen', False):
        os.chdir(os.path.join(BASE_DIR, '_internal'))

    call_command(
        'runserver',
        '127.0.0.1:8000',
        '--noreload',
        '--nothreading'
    )


def attendre_serveur():
    """Attend que Django soit prêt"""
    import urllib.request
    for i in range(60):  # 30 secondes max
        try:
            urllib.request.urlopen(
                'http://127.0.0.1:8000/accounts/login/',
                timeout=1
            )
            return True
        except:
            time.sleep(0.5)
    return False


if __name__ == '__main__':

    print("Initialisation de la base de données...")
    initialiser_base()

    print("Démarrage du serveur Django...")
    thread_django = threading.Thread(
        target=demarrer_django,
        daemon=True
    )
    thread_django.start()

    print("En attente du serveur...")
    serveur_pret = attendre_serveur()

    if not serveur_pret:
        print("Erreur : impossible de démarrer le serveur.")
        sys.exit(1)

    print("Serveur prêt !")

    # Démarrer la sync en arrière-plan
    thread_sync = threading.Thread(
        target=synchronisation_periodique,
        daemon=True
    )
    thread_sync.start()

    # Ouvrir la fenêtre
    window = webview.create_window(
        title='Bignon AquaStock',
        url='http://127.0.0.1:8000/',
        width=1280,
        height=800,
        min_size=(1024, 600),
        resizable=True,
    )

    webview.start(debug=False)