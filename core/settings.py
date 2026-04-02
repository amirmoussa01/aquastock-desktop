from pathlib import Path
import sys
import os

# Compatibilité PyInstaller
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(os.path.dirname(sys.executable))
    INTERNAL_DIR = BASE_DIR / '_internal'
else:
    BASE_DIR = Path(__file__).resolve().parent.parent
    INTERNAL_DIR = BASE_DIR

SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'bignon-aquastock-secret-key-change-en-production-2026'
)

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Nos applications
    'accounts',
    'produits',
    'stock',
    'ventes',
    'rapports',
    'depenses',
    'sync',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [INTERNAL_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Base de données SQLite locale
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Validation mots de passe
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
]

# Langue et timezone
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Porto-Novo'
USE_I18N = True
USE_TZ = True

# Fichiers statiques (CSS, JS, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [INTERNAL_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Fichiers media (photos produits)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Modèle utilisateur personnalisé
AUTH_USER_MODEL = 'accounts.Utilisateur'

# Redirection après login/logout
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Devise
DEVISE = 'FCFA'
NOM_ENTREPRISE = 'Bignon AquaStock'

# ─────────────────────────────────────
# Synchronisation serveur
# ─────────────────────────────────────
SERVEUR_URL   = 'https://app-03e4d217-5880-4510-b79f-957dbffd2c21.cleverapps.io'
MACHINE_ID    = 'machine_01'
SYNC_TOKEN    = '9cbfd26248df004c518b4f03c7fe33604e48c02f'
SYNC_INTERVAL = 300  # 5 minutes entre chaque sync automatique