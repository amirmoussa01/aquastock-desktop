// ─── Sync Status & Manuel – Bignon AquaStock ───────────────────
(function () {
    var INTERVAL_MS = 60000; // verifier toutes les 60s
    var syncing = false;

    function verifierSync() {
        fetch('/sync/statut/', { credentials: 'same-origin' })
            .then(function (r) { return r.json(); })
            .then(function (data) {
                var el = document.getElementById('sync-indicator');
                var txt = document.getElementById('sync-text');
                if (!el) return;

                if (data.synced) {
                    el.className = 'badge rounded-pill bg-success ms-2';
                    el.title = 'Synchronise – ' + data.derniere_sync;
                    if (txt) txt.textContent = 'Sync OK';
                } else {
                    el.className = 'badge rounded-pill bg-danger ms-2';
                    el.title = data.details
                        ? (data.details.ventes + ' ventes, ' + data.details.depenses + ' depenses non sync')
                        : 'En attente de synchronisation';
                    if (txt) txt.textContent = data.non_synced + ' en attente';
                }
            })
            .catch(function () {
                var el = document.getElementById('sync-indicator');
                if (!el) return;
                el.className = 'badge rounded-pill bg-secondary ms-2';
                el.title = 'Connexion au serveur impossible';
                var txt = document.getElementById('sync-text');
                if (txt) txt.textContent = 'Hors ligne';
            });
    }

    function lancerSync() {
        if (syncing) return;
        syncing = true;
        var btn = document.getElementById('btn-sync');
        var el  = document.getElementById('sync-indicator');
        if (btn) {
            btn.disabled = true;
            btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>Sync...';
        }
        if (el) el.className = 'badge rounded-pill bg-warning ms-2';

        fetch('/sync/lancer/', {
            method: 'POST',
            credentials: 'same-origin',
            headers: { 'X-CSRFToken': getCookie('csrftoken') }
        })
            .then(function (r) { return r.json(); })
            .then(function () {
                // Attendre 4s puis revérifier
                setTimeout(function () {
                    verifierSync();
                    syncing = false;
                    if (btn) {
                        btn.disabled = false;
                        btn.innerHTML = '<i class="bi bi-arrow-repeat me-1"></i>Synchroniser';
                    }
                }, 4000);
            })
            .catch(function () {
                syncing = false;
                if (btn) {
                    btn.disabled = false;
                    btn.innerHTML = '<i class="bi bi-arrow-repeat me-1"></i>Synchroniser';
                }
                verifierSync();
            });
    }

    function getCookie(name) {
        var v = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
        return v ? v[2] : '';
    }

    // Init
    document.addEventListener('DOMContentLoaded', function () {
        var btn = document.getElementById('btn-sync');
        if (btn) btn.addEventListener('click', lancerSync);
        verifierSync();
        setInterval(verifierSync, INTERVAL_MS);
    });
})();
