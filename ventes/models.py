from django.db import models
from accounts.models import Utilisateur
from produits.models import Produit
import uuid


class Vente(models.Model):

    MODE_PAIEMENT = (
        ('cash', 'Cash'),
        ('mobile_money', 'Mobile Money'),
    )

    STATUT = (
        ('validee', 'Validée'),
        ('annulee', 'Annulée'),
    )

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    reference = models.CharField(max_length=50, unique=True)
    vendeur = models.ForeignKey(
        Utilisateur, on_delete=models.PROTECT, related_name='ventes'
    )
    mode_paiement = models.CharField(
        max_length=20, choices=MODE_PAIEMENT, default='cash'
    )
    statut = models.CharField(
        max_length=20, choices=STATUT, default='validee'
    )
    montant_total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    note = models.TextField(blank=True, null=True)
    date_vente = models.DateTimeField(auto_now_add=True)
    synced = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Vente'
        verbose_name_plural = 'Ventes'
        ordering = ['-date_vente']

    def __str__(self):
        return f"Vente {self.reference} – {self.montant_total} FCFA"

    def save(self, *args, **kwargs):
        if not self.reference:
            import datetime
            now = datetime.datetime.now()
            self.reference = f"VTE-{now.strftime('%Y%m%d%H%M%S')}"
        super().save(*args, **kwargs)


class LigneVente(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    vente = models.ForeignKey(
        Vente, on_delete=models.CASCADE, related_name='lignes'
    )
    produit = models.ForeignKey(
        Produit, on_delete=models.PROTECT, related_name='lignes_vente'
    )
    quantite = models.DecimalField(max_digits=10, decimal_places=2)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    sous_total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Ligne de Vente'
        verbose_name_plural = 'Lignes de Vente'

    def __str__(self):
        return f"{self.produit.nom} x{self.quantite}"

    def save(self, *args, **kwargs):
        self.sous_total = self.quantite * self.prix_unitaire
        super().save(*args, **kwargs)
