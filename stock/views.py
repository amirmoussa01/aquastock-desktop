from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.decorators import gestionnaire_requis
from .models import MouvementStock
from produits.models import Produit


@login_required
def liste_mouvements(request):
    from django.core.paginator import Paginator

    mouvements_liste = MouvementStock.objects.select_related(
        'produit', 'utilisateur'
    ).order_by('-date_mouvement')

    paginator = Paginator(mouvements_liste, 20)
    page = request.GET.get('page')
    mouvements = paginator.get_page(page)

    return render(request, 'stock/liste.html', {'mouvements': mouvements})


@gestionnaire_requis
def historique(request):
    from django.core.paginator import Paginator

    mouvements_liste = MouvementStock.objects.select_related(
        'produit', 'utilisateur'
    ).order_by('-date_mouvement')

    # Filtre par produit
    produit_id = request.GET.get('produit', '')
    if produit_id:
        mouvements_liste = mouvements_liste.filter(produit_id=produit_id)

    paginator = Paginator(mouvements_liste, 20)
    page = request.GET.get('page')
    mouvements = paginator.get_page(page)
    produits = Produit.objects.filter(est_actif=True)

    return render(request, 'stock/historique.html', {
        'mouvements': mouvements,
        'produits': produits,
        'produit_id': produit_id,
    })

@gestionnaire_requis
def entree_stock(request):
    from decimal import Decimal

    produits = Produit.objects.filter(est_actif=True)
    if request.method == 'POST':
        produit_id = request.POST.get('produit')
        quantite = Decimal(str(request.POST.get('quantite', 0)))
        motif = request.POST.get('motif', 'Livraison fournisseur')
        try:
            produit = Produit.objects.get(pk=produit_id)
            stock_avant = produit.stock_actuel
            produit.stock_actuel = stock_avant + quantite
            produit.save()

            MouvementStock.objects.create(
                produit=produit,
                type_mouvement='entree',
                quantite=quantite,
                stock_avant=stock_avant,
                stock_apres=produit.stock_actuel,
                motif=motif,
                utilisateur=request.user,
            )
            messages.success(
                request,
                f'Entrée de {quantite} {produit.unite} enregistrée.'
            )
            return redirect('stock:liste')
        except Exception as e:
            messages.error(request, f'Erreur : {e}')

    return render(request, 'stock/entree.html', {'produits': produits})


