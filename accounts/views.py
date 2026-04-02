from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_requis
from .models import Utilisateur


def login_view(request):
    if request.user.is_authenticated:
        return redirect('produits:dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.est_actif:
                login(request, user)
                return redirect('produits:dashboard')
            else:
                messages.error(request, 'Votre compte est désactivé.')
        else:
            messages.error(request, 'Identifiant ou mot de passe incorrect.')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('accounts:login')


@admin_requis
def liste_utilisateurs(request):
    utilisateurs = Utilisateur.objects.all().order_by('role', 'username')
    return render(request, 'accounts/utilisateurs/liste.html', {
        'utilisateurs': utilisateurs
    })


@admin_requis
def ajouter_utilisateur(request):
    if request.method == 'POST':
        try:
            username   = request.POST.get('username')
            prenom     = request.POST.get('first_name')
            nom        = request.POST.get('last_name')
            telephone  = request.POST.get('telephone')
            role       = request.POST.get('role')
            password   = request.POST.get('password')
            password2  = request.POST.get('password2')

            if password != password2:
                messages.error(request, 'Les mots de passe ne correspondent pas.')
                return render(request, 'accounts/utilisateurs/form.html')

            if Utilisateur.objects.filter(username=username).exists():
                messages.error(request, f'L\'identifiant "{username}" est déjà utilisé.')
                return render(request, 'accounts/utilisateurs/form.html')

            user = Utilisateur.objects.create_user(
                username=username,
                password=password,
                first_name=prenom,
                last_name=nom,
                telephone=telephone,
                role=role,
            )
            messages.success(request, f'Utilisateur "{user.get_full_name()}" créé avec succès.')
            return redirect('accounts:utilisateurs')

        except Exception as e:
            messages.error(request, f'Erreur : {e}')

    return render(request, 'accounts/utilisateurs/form.html')


@admin_requis
def modifier_utilisateur(request, pk):
    utilisateur = get_object_or_404(Utilisateur, pk=pk)

    if request.method == 'POST':
        try:
            utilisateur.first_name = request.POST.get('first_name')
            utilisateur.last_name  = request.POST.get('last_name')
            utilisateur.telephone  = request.POST.get('telephone')
            utilisateur.role       = request.POST.get('role')

            # Changer mot de passe seulement si rempli
            password = request.POST.get('password')
            if password:
                password2 = request.POST.get('password2')
                if password != password2:
                    messages.error(request, 'Les mots de passe ne correspondent pas.')
                    return render(request, 'accounts/utilisateurs/form.html', {
                        'utilisateur': utilisateur
                    })
                utilisateur.set_password(password)

            utilisateur.save()
            messages.success(request, f'Utilisateur "{utilisateur.get_full_name()}" modifié.')
            return redirect('accounts:utilisateurs')

        except Exception as e:
            messages.error(request, f'Erreur : {e}')

    return render(request, 'accounts/utilisateurs/form.html', {
        'utilisateur': utilisateur
    })


@admin_requis
def toggle_utilisateur(request, pk):
    utilisateur = get_object_or_404(Utilisateur, pk=pk)

    # Empêcher de désactiver son propre compte
    if utilisateur == request.user:
        messages.error(request, 'Vous ne pouvez pas désactiver votre propre compte.')
        return redirect('accounts:utilisateurs')

    utilisateur.est_actif = not utilisateur.est_actif
    utilisateur.save()

    etat = 'activé' if utilisateur.est_actif else 'désactivé'
    messages.success(request, f'Compte de "{utilisateur.get_full_name()}" {etat}.')
    return redirect('accounts:utilisateurs')

def splash_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    return render(request, 'splash.html')


