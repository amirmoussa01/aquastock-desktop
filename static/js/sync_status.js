function verifierSync() {
    fetch('/sync/statut/')
        .then(response => response.json())
        .then(data => {
            const indicator = document.getElementById('sync-indicator');
            if (data.synced) {
                indicator.classList.remove('bg-danger');
                indicator.classList.add('bg-success');
                indicator.title = 'Synchronisé - ' + data.derniere_sync;
            } else {
                indicator.classList.remove('bg-success');
                indicator.classList.add('bg-danger');
                indicator.title = 'En attente de synchronisation';
            }
        })
        .catch(() => {
            const indicator = document.getElementById('sync-indicator');
            indicator.classList.remove('bg-success');
            indicator.classList.add('bg-secondary');
            indicator.title = 'Serveur non accessible';
        });
}

// Vérifie toutes les 30 secondes
verifierSync();
setInterval(verifierSync, 30000);