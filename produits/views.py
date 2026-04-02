from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import gestionnaire_requis, admin_requis
from .models import Produit, Categorie


@login_required
def dashboard(request):
    from ventes.models import Vente, LigneVente
    from stock.models import MouvementStock
    from depenses.models import Depense
    from django.utils import timezone
    from django.db.models import Sum, Count

    aujourd_hui = timezone.now().date()

    # ── Produits ──────────────────────────────
    total_produits = Produit.objects.filter(est_actif=True).count()
    alertes_stock  = [p for p in Produit.objects.filter(est_actif=True) if p.stock_faible()]

    # ── Ventes du jour ────────────────────────
    ventes_jour_qs = Vente.objects.filter(
        date_vente__date=aujourd_hui,
        statut='validee'
    )
    nb_ventes_jour = ventes_jour_qs.count()
    total_jour     = ventes_jour_qs.aggregate(
        total=Sum('montant_total')
    )['total'] or 0

    # ── Dépenses du jour ──────────────────────
    depenses_jour = Depense.objects.filter(
        date_depense__date=aujourd_hui
    ).aggregate(total=Sum('montant'))['total'] or 0

    # ── Bénéfice du jour ──────────────────────
    benefice_jour = total_jour - depenses_jour

    # ── Ventes du mois ────────────────────────
    ventes_mois_qs = Vente.objects.filter(
        date_vente__year=aujourd_hui.year,
        date_vente__month=aujourd_hui.month,
        statut='validee'
    )
    total_mois = ventes_mois_qs.aggregate(
        total=Sum('montant_total')
    )['total'] or 0

    # ── 5 dernières ventes ────────────────────
    dernieres_ventes = Vente.objects.filter(
        statut='validee'
    ).select_related('vendeur').order_by('-date_vente')[:5]

    # ── Produits les plus vendus ──────────────
    top_produits = LigneVente.objects.filter(
        vente__statut='validee',
        vente__date_vente__date=aujourd_hui
    ).values(
        'produit__nom'
    ).annotate(
        total_qte=Sum('quantite')
    ).order_by('-total_qte')[:5]

    context = {
        'total_produits'  : total_produits,
        'alertes_stock'   : alertes_stock,
        'nb_alertes'      : len(alertes_stock),
        'nb_ventes_jour'  : nb_ventes_jour,
        'total_jour'      : total_jour,
        'depenses_jour'   : depenses_jour,
        'benefice_jour'   : benefice_jour,
        'total_mois'      : total_mois,
        'dernieres_ventes': dernieres_ventes,
        'top_produits'    : top_produits,
    }
    return render(request, 'produits/dashboard.html', context)

@gestionnaire_requis
def liste_produits(request):
    from django.core.paginator import Paginator

    produits_liste = Produit.objects.filter(
        est_actif=True
    ).select_related('categorie').order_by('nom')

    # Recherche
    recherche = request.GET.get('q', '')
    if recherche:
        produits_liste = produits_liste.filter(nom__icontains=recherche)

    paginator = Paginator(produits_liste, 15)  # 15 par page
    page = request.GET.get('page')
    produits = paginator.get_page(page)

    return render(request, 'produits/liste.html', {
        'produits': produits,
        'recherche': recherche,
    })

@gestionnaire_requis
def ajouter_produit(request):
    categories = Categorie.objects.all()
    if request.method == 'POST':
        try:
            produit = Produit(
                nom=request.POST.get('nom'),
                categorie_id=request.POST.get('categorie'),
                description=request.POST.get('description'),
                prix_achat=request.POST.get('prix_achat'),
                prix_vente=request.POST.get('prix_vente'),
                stock_actuel=request.POST.get('stock_actuel', 0),
                seuil_alerte=request.POST.get('seuil_alerte', 5),
                unite=request.POST.get('unite', 'kg'),
            )
            if request.FILES.get('image'):
                produit.image = request.FILES['image']
            produit.save()
            messages.success(request, f'Produit "{produit.nom}" ajouté avec succès.')
            return redirect('produits:liste')
        except Exception as e:
            messages.error(request, f'Erreur : {e}')

    return render(request, 'produits/form.html', {'categories': categories})


@gestionnaire_requis
def modifier_produit(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    categories = Categorie.objects.all()
    if request.method == 'POST':
        try:
            produit.nom = request.POST.get('nom')
            produit.categorie_id = request.POST.get('categorie')
            produit.description = request.POST.get('description')
            produit.prix_achat = request.POST.get('prix_achat')
            produit.prix_vente = request.POST.get('prix_vente')
            produit.seuil_alerte = request.POST.get('seuil_alerte', 5)
            produit.unite = request.POST.get('unite', 'kg')
            if request.FILES.get('image'):
                produit.image = request.FILES['image']
            produit.save()
            messages.success(request, f'Produit "{produit.nom}" modifié.')
            return redirect('produits:liste')
        except Exception as e:
            messages.error(request, f'Erreur : {e}')

    return render(request, 'produits/form.html', {
        'produit': produit,
        'categories': categories
    })


@admin_requis
def supprimer_produit(request, pk):
    produit = get_object_or_404(Produit, pk=pk)
    if request.method == 'POST':
        produit.est_actif = False
        produit.save()
        messages.success(request, f'Produit "{produit.nom}" supprimé.')
        return redirect('produits:liste')
    return render(request, 'produits/confirmer_suppression.html', {'produit': produit})


@gestionnaire_requis
def liste_categories(request):
    categories = Categorie.objects.all()
    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description', '')
        if nom:
            Categorie.objects.create(nom=nom, description=description)
            messages.success(request, f'Catégorie "{nom}" ajoutée.')
            return redirect('produits:categories')
    return render(request, 'produits/categories.html', {'categories': categories})
