import urllib.request
import urllib.error
import json
import time


def get_config():
    from django.conf import settings
    return {
        'serveur_url': getattr(settings, 'SERVEUR_URL', 'http://127.0.0.1:8001'),
        'machine_id':  getattr(settings, 'MACHINE_ID', 'machine_01'),
        'token':       getattr(settings, 'SYNC_TOKEN', None),
    }


def reveiller_serveur(serveur_url):
    for tentative in range(3):
        try:
            urllib.request.urlopen(
                f'{serveur_url}/api/ping/',
                timeout=20
            )
            print("Serveur accessible.")
            return True
        except urllib.error.HTTPError:
            print("Serveur accessible (HTTP).")
            return True
        except Exception as e:
            print(f"Tentative {tentative + 1}/3 echouee : {e}")
            time.sleep(5)
    return False


def envoyer_donnees(serveur_url, token, machine_id, donnees):
    try:
        data = json.dumps({
            'machine_id': machine_id,
            'donnees':    donnees
        }, default=str).encode()

        req = urllib.request.Request(
            f'{serveur_url}/api/sync/',
            data=data,
            headers={
                'Content-Type':  'application/json',
                'Authorization': f'Token {token}'
            },
            method='POST'
        )
        response = urllib.request.urlopen(req, timeout=30)
        return json.loads(response.read().decode())
    except Exception as e:
        print(f'Erreur envoi : {e}')
        return None


def telecharger_donnees(serveur_url, token):
    """Telecharge toutes les donnees du serveur vers le Desktop"""
    try:
        req = urllib.request.Request(
            f'{serveur_url}/api/descendante/',
            headers={
                'Content-Type':  'application/json',
                'Authorization': f'Token {token}'
            },
            method='GET'
        )
        response = urllib.request.urlopen(req, timeout=30)
        return json.loads(response.read().decode())
    except Exception as e:
        print(f'Erreur telechargement : {e}')
        return None


def appliquer_donnees(donnees):
    """Applique toutes les donnees du serveur sur la base locale"""
    from produits.models import Produit, Categorie
    from ventes.models import Vente, LigneVente
    from depenses.models import Depense
    from accounts.models import Utilisateur

    stats = {
        'categories':    0,
        'produits':      0,
        'utilisateurs':  0,
        'ventes':        0,
        'depenses':      0,
    }

    # 1. Categories
    for c in donnees.get('categories', []):
        Categorie.objects.update_or_create(
            uuid=c['uuid'],
            defaults={
                'nom':         c['nom'],
                'description': c.get('description', ''),
            }
        )
        stats['categories'] += 1

    # 2. Produits
    for p in donnees.get('produits', []):
        try:
            categorie = Categorie.objects.get(uuid=p['categorie_uuid'])
            Produit.objects.update_or_create(
                uuid=p['uuid'],
                defaults={
                    'nom':          p['nom'],
                    'categorie':    categorie,
                    'prix_achat':   p['prix_achat'],
                    'prix_vente':   p['prix_vente'],
                    'stock_actuel': p['stock_actuel'],
                    'seuil_alerte': p['seuil_alerte'],
                    'unite':        p['unite'],
                    'est_actif':    p['est_actif'],
                }
            )
            stats['produits'] += 1
        except Categorie.DoesNotExist:
            print(f"Categorie introuvable pour produit {p['nom']}")

    # 3. Utilisateurs
    for u in donnees.get('utilisateurs', []):
        utilisateur, created = Utilisateur.objects.get_or_create(
            username=u['username'],
            defaults={
                'first_name': u['first_name'],
                'last_name':  u['last_name'],
                'role':       u['role'],
                'est_actif':  u['est_actif'],
            }
        )
        if created:
            # Copie le hash du mot de passe directement
            utilisateur.password = u['password_hash']
            utilisateur.save()
            stats['utilisateurs'] += 1

    # 4. Ventes
    for v in donnees.get('ventes', []):
        if Vente.objects.filter(uuid=v['uuid']).exists():
            continue
        try:
            vendeur = Utilisateur.objects.get(username=v['vendeur_username'])
            vente = Vente.objects.create(
                uuid=          v['uuid'],
                reference=     v['reference'],
                vendeur=       vendeur,
                mode_paiement= v['mode_paiement'],
                statut=        v['statut'],
                montant_total= v['montant_total'],
                synced=        True,
            )
            for l in v.get('lignes', []):
                try:
                    produit = Produit.objects.get(uuid=l['produit_uuid'])
                    LigneVente.objects.create(
                        uuid=          l['uuid'],
                        vente=         vente,
                        produit=       produit,
                        quantite=      l['quantite'],
                        prix_unitaire= l['prix_unitaire'],
                        sous_total=    l['sous_total'],
                    )
                except Produit.DoesNotExist:
                    pass
            stats['ventes'] += 1
        except Utilisateur.DoesNotExist:
            pass

    # 5. Depenses
    for d in donnees.get('depenses', []):
        if Depense.objects.filter(uuid=d['uuid']).exists():
            continue
        try:
            enregistre_par = Utilisateur.objects.get(
                username=d['enregistre_par_username']
            )
            Depense.objects.create(
                uuid=              d['uuid'],
                categorie=         d['categorie'],
                description=       d['description'],
                montant=           d['montant'],
                enregistre_par=    enregistre_par,
                note=              d.get('note', ''),
                synced=            True,
            )
            stats['depenses'] += 1
        except Utilisateur.DoesNotExist:
            pass

    print(f"Donnees appliquees : {stats}")
    return stats


def synchroniser():
    """
    Sync complete bidirectionnelle :
    1. Envoie les donnees locales non sync vers le serveur
    2. Recupere toutes les donnees du serveur
    3. Applique sur la base locale
    """
    from produits.models import Produit, Categorie
    from ventes.models import Vente
    from depenses.models import Depense

    cfg = get_config()
    print(f"Serveur cible : {cfg['serveur_url']}")

    if not cfg['token']:
        return {'statut': 'erreur', 'message': 'Token non configure.'}

    # Reveille le serveur
    print("Reveil du serveur...")
    if not reveiller_serveur(cfg['serveur_url']):
        return {'statut': 'offline', 'message': 'Serveur non accessible.'}

    # Donnees a envoyer (montant local non sync)
    ventes   = Vente.objects.filter(synced=False).prefetch_related('lignes__produit')
    depenses = Depense.objects.filter(synced=False)

    print(f"{ventes.count()} ventes a envoyer")
    print(f"{depenses.count()} depenses a envoyer")

    categories = Categorie.objects.all()
    produits   = Produit.objects.filter(est_actif=True)

    donnees_upload = {
        'categories': [
            {
                'uuid':        str(c.uuid),
                'nom':         c.nom,
                'description': c.description or '',
            }
            for c in categories
        ],
        'produits': [
            {
                'uuid':           str(p.uuid),
                'nom':            p.nom,
                'categorie_uuid': str(p.categorie.uuid),
                'prix_achat':     float(p.prix_achat),
                'prix_vente':     float(p.prix_vente),
                'stock_actuel':   float(p.stock_actuel),
                'seuil_alerte':   float(p.seuil_alerte),
                'unite':          p.unite,
                'est_actif':      p.est_actif,
            }
            for p in produits
        ],
        'ventes': [
            {
                'uuid':             str(v.uuid),
                'reference':        v.reference,
                'vendeur_username': v.vendeur.username,
                'mode_paiement':    v.mode_paiement,
                'statut':           v.statut,
                'montant_total':    float(v.montant_total),
                'date_vente':       str(v.date_vente),
                'lignes': [
                    {
                        'uuid':          str(l.uuid),
                        'produit_uuid':  str(l.produit.uuid),
                        'quantite':      float(l.quantite),
                        'prix_unitaire': float(l.prix_unitaire),
                        'sous_total':    float(l.sous_total),
                    }
                    for l in v.lignes.all()
                ]
            }
            for v in ventes
        ],
        'depenses': [
            {
                'uuid':                    str(d.uuid),
                'categorie':               d.categorie,
                'description':             d.description,
                'montant':                 float(d.montant),
                'enregistre_par_username': d.enregistre_par.username,
                'note':                    d.note or '',
                'date_depense':            str(d.date_depense),
            }
            for d in depenses
        ],
    }

    # 1. Envoie vers le serveur
    resultat = envoyer_donnees(
        cfg['serveur_url'],
        cfg['token'],
        cfg['machine_id'],
        donnees_upload
    )
    print(f"Reponse serveur : {resultat}")

    if resultat and resultat.get('statut') == 'success':
        ventes.update(synced=True)
        depenses.update(synced=True)

    # 2. Telecharge tout depuis le serveur
    print("Telechargement donnees serveur...")
    data = telecharger_donnees(cfg['serveur_url'], cfg['token'])

    if data and data.get('statut') == 'success':
        stats = appliquer_donnees(data['donnees'])
        return {
            'statut':  'success',
            'message': 'Synchronisation complete reussie !',
            'details': stats,
        }

    return {
        'statut':  'erreur',
        'message': f"Echec telechargement : {data}"
    }