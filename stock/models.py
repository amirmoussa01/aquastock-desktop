from django.db import models
from accounts.models import Utilisateur
from produits.models import Produit
import uuid


class MouvementStock(models.Model):

    TYPE_MOUVEMENT = (
        ('entree', 'Entrée stock'),
        ('sortie', 'Sortie stock'),
        ('ajustement', 'Ajustement'),
    )

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    produit = models.ForeignKey(
        Produit, on_delete=models.PROTECT, related_name='mouvements'
    )
    type_mouvement = models.CharField(max_length=20, choices=TYPE_MOUVEMENT)
    quantite = models.DecimalField(max_digits=10, decimal_places=2)
    stock_avant = models.DecimalField(max_digits=10, decimal_places=2)
    stock_apres = models.DecimalField(max_digits=10, decimal_places=2)
    motif = models.CharField(max_length=255, blank=True, null=True)
    utilisateur = models.ForeignKey(
        Utilisateur, on_delete=models.PROTECT, related_name='mouvements'
    )
    date_mouvement = models.DateTimeField(auto_now_add=True)
    synced = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Mouvement Stock'
        verbose_name_plural = 'Mouvements Stock'
        ordering = ['-date_mouvement']

    def __str__(self):
        return f"{self.type_mouvement} – {self.produit.nom} – {self.quantite}"
