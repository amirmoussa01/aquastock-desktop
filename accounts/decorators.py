from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def admin_requis(fonction):
    @wraps(fonction)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if request.user.role != 'admin':
            messages.error(request, 'Accès réservé aux administrateurs.')
            return redirect('produits:dashboard')
        return fonction(request, *args, **kwargs)
    return wrapper


def gestionnaire_requis(fonction):
    @wraps(fonction)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if request.user.role not in ['admin', 'gestionnaire']:
            messages.error(request, 'Accès non autorisé.')
            return redirect('produits:dashboard')
        return fonction(request, *args, **kwargs)
    return wrapper


def vendeur_requis(fonction):
    @wraps(fonction)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if request.user.role not in ['admin', 'gestionnaire', 'vendeur']:
            messages.error(request, 'Accès non autorisé.')
            return redirect('accounts:login')
        return fonction(request, *args, **kwargs)
    return wrapper

