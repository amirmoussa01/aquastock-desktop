from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import admin_requis
from .models import Vente, LigneVente
from produits.models import Produit
from stock.models import MouvementStock


@login_required
def liste_ventes(request):
    from django.core.paginator import Paginator

    if request.user.role == 'vendeur':
        ventes_liste = Vente.objects.filter(
            vendeur=request.user
        ).select_related('vendeur').order_by('-date_vente')
    else:
        ventes_liste = Vente.objects.select_related(
            'vendeur'
        ).order_by('-date_vente')

    # Filtre par date
    date_filtre = request.GET.get('date', '')
    if date_filtre:
        ventes_liste = ventes_liste.filter(
            date_vente__date=date_filtre
        )

    paginator = Paginator(ventes_liste, 20)
    page = request.GET.get('page')
    ventes = paginator.get_page(page)

    return render(request, 'ventes/liste.html', {
        'ventes': ventes,
        'date_filtre': date_filtre,
    })

@login_required
def nouvelle_vente(request):
    from decimal import Decimal

    produits = Produit.objects.filter(est_actif=True, stock_actuel__gt=0)
    if request.method == 'POST':
        mode_paiement = request.POST.get('mode_paiement', 'cash')
        produits_ids = request.POST.getlist('produit_id')
        quantites = request.POST.getlist('quantite')

        if not produits_ids:
            messages.error(request, 'Ajoutez au moins un produit.')
            return render(request, 'ventes/nouvelle.html', {'produits': produits})

        try:
            vente = Vente.objects.create(
                vendeur=request.user,
                mode_paiement=mode_paiement,
                montant_total=0,
            )
            total = Decimal('0')

            for pid, qte in zip(produits_ids, quantites):
                produit = Produit.objects.get(pk=pid)
                qte = Decimal(str(qte))
                sous_total = qte * produit.prix_vente
                total += sous_total

                LigneVente.objects.create(
                    vente=vente,
                    produit=produit,
                    quantite=qte,
                    prix_unitaire=produit.prix_vente,
                    sous_total=sous_total,
                )

                # Mise à jour stock
                stock_avant = produit.stock_actuel
                produit.stock_actuel = stock_avant - qte
                produit.save()

                MouvementStock.objects.create(
                    produit=produit,
                    type_mouvement='sortie',
                    quantite=qte,
                    stock_avant=stock_avant,
                    stock_apres=produit.stock_actuel,
                    motif=f'Vente {vente.reference}',
                    utilisateur=request.user,
                )

            vente.montant_total = total
            vente.save()
            messages.success(request, f'Vente {vente.reference} enregistrée !')
            return redirect('ventes:ticket', pk=vente.pk)

        except Exception as e:
            messages.error(request, f'Erreur : {e}')

    return render(request, 'ventes/nouvelle.html', {'produits': produits})

@login_required
def ticket_vente(request, pk):
    vente = get_object_or_404(Vente, pk=pk)
    # Vendeur peut voir seulement ses tickets
    if request.user.role == 'vendeur' and vente.vendeur != request.user:
        messages.error(request, 'Accès non autorisé.')
        return redirect('ventes:liste')
    lignes = vente.lignes.select_related('produit').all()
    return render(request, 'ventes/ticket.html', {'vente': vente, 'lignes': lignes})


@admin_requis
def annuler_vente(request, pk):
    vente = get_object_or_404(Vente, pk=pk)
    if request.method == 'POST':
        vente.statut = 'annulee'
        vente.save()
        messages.success(request, f'Vente {vente.reference} annulée.')
        return redirect('ventes:liste')
    return render(request, 'ventes/annuler.html', {'vente': vente})
