from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from ventes.models import Vente
from depenses.models import Depense
from django.utils import timezone


@login_required
def statut_sync(request):
    non_synced_ventes = Vente.objects.filter(synced=False).count()
    non_synced_depenses = Depense.objects.filter(synced=False).count()
    total_non_synced = non_synced_ventes + non_synced_depenses

    return JsonResponse({
        'synced': total_non_synced == 0,
        'non_synced': total_non_synced,
        'derniere_sync': str(timezone.now().strftime('%d/%m/%Y %H:%M')),
    })

