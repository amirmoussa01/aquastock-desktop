from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from accounts.decorators import gestionnaire_requis, admin_requis
from .models import Depense
from django.db.models import Sum


@gestionnaire_requis
def liste_depenses(request):
    from django.core.paginator import Paginator
    from django.utils import timezone

    aujourd_hui = timezone.now().date()
    depenses_liste = Depense.objects.select_related(
        'enregistre_par'
    ).order_by('-date_depense')

    # Filtre par catégorie
    categorie_filtre = request.GET.get('categorie', '')
    if categorie_filtre:
        depenses_liste = depenses_liste.filter(categorie=categorie_filtre)

    total_jour = Depense.objects.filter(
        date_depense__date=aujourd_hui
    ).aggregate(
        total=Sum('montant')
    )['total'] or 0

    total_global = Depense.objects.aggregate(
        total=Sum('montant')
    )['total'] or 0

    paginator = Paginator(depenses_liste, 20)
    page = request.GET.get('page')
    depenses = paginator.get_page(page)

    return render(request, 'depenses/liste.html', {
        'depenses': depenses,
        'total_jour': total_jour,
        'total_global': total_global,
        'categories': Depense.CATEGORIES,
        'categorie_filtre': categorie_filtre,
    })

@gestionnaire_requis
def ajouter_depense(request):
    if request.method == 'POST':
        try:
            Depense.objects.create(
                categorie=request.POST.get('categorie'),
                description=request.POST.get('description'),
                montant=request.POST.get('montant'),
                note=request.POST.get('note', ''),
                enregistre_par=request.user,
            )
            messages.success(request, 'Dépense enregistrée avec succès.')
            return redirect('depenses:liste')
        except Exception as e:
            messages.error(request, f'Erreur : {e}')

    return render(request, 'depenses/form.html', {
        'categories': Depense.CATEGORIES
    })


@admin_requis
def supprimer_depense(request, pk):
    depense = get_object_or_404(Depense, pk=pk)
    if request.method == 'POST':
        depense.delete()
        messages.success(request, 'Dépense supprimée.')
        return redirect('depenses:liste')
    return render(request, 'depenses/confirmer_suppression.html', {
        'depense': depense
    })