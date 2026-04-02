import os
import sys

# Définir le dossier de base quand on est en .exe
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
    os.environ['DJANGO_BASE_DIR'] = BASE_DIR