from django.shortcuts import render
from django.utils import timezone
from accounts.decorators import gestionnaire_requis
from ventes.models import Vente


@gestionnaire_requis
def rapport_journalier(request):
    aujourd_hui = timezone.now().date()
    ventes = Vente.objects.filter(
        date_vente__date=aujourd_hui,
        statut='validee'
    ).select_related('vendeur')
    total_jour = sum(v.montant_total for v in ventes)
    return render(request, 'rapports/journalier.html', {
        'ventes': ventes,
        'total_jour': total_jour,
        'date': aujourd_hui,
    })


@gestionnaire_requis
def rapport_mensuel(request):
    aujourd_hui = timezone.now()
    ventes = Vente.objects.filter(
        date_vente__year=aujourd_hui.year,
        date_vente__month=aujourd_hui.month,
        statut='validee'
    ).select_related('vendeur')
    total_mois = sum(v.montant_total for v in ventes)
    return render(request, 'rapports/mensuel.html', {
        'ventes': ventes,
        'total_mois': total_mois,
        'mois': aujourd_hui.strftime('%B %Y'),
    })

