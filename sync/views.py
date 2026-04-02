import threading
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from ventes.models import Vente
from depenses.models import Depense
from stock.models import MouvementStock


@login_required
def statut_sync(request):
    non_synced_ventes    = Vente.objects.filter(synced=False).count()
    non_synced_depenses  = Depense.objects.filter(synced=False).count()
    non_synced_mouvements = MouvementStock.objects.filter(synced=False).count()
    total_non_synced = non_synced_ventes + non_synced_depenses + non_synced_mouvements

    return JsonResponse({
        'synced':       total_non_synced == 0,
        'non_synced':   total_non_synced,
        'details': {
            'ventes':     non_synced_ventes,
            'depenses':   non_synced_depenses,
            'mouvements': non_synced_mouvements,
        },
        'derniere_sync': str(timezone.now().strftime('%d/%m/%Y %H:%M')),
    })


@login_required
def lancer_sync(request):
    """Lance une synchronisation manuelle en arriere-plan"""
    if request.method != 'POST':
        return JsonResponse({'statut': 'erreur', 'message': 'Methode non autorisee.'}, status=405)

    def do_sync():
        try:
            from sync.service import synchroniser
            synchroniser()
        except Exception as e:
            print(f"Erreur sync manuelle : {e}")

    t = threading.Thread(target=do_sync, daemon=True)
    t.start()

    return JsonResponse({'statut': 'ok', 'message': 'Synchronisation lancee en arriere-plan.'})
