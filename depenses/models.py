from django.db import models
from accounts.models import Utilisateur
import uuid


class Depense(models.Model):

    CATEGORIES = (
        ('achat_stock',   'Achat stock/fournisseur'),
        ('transport',     'Transport'),
        ('salaire',       'Salaire employé'),
        ('electricite',   'Électricité'),
        ('eau',           'Eau'),
        ('loyer',         'Loyer'),
        ('materiel',      'Matériel'),
        ('autre',         'Autre'),
    )

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    categorie = models.CharField(
        max_length=50, choices=CATEGORIES, default='autre'
    )
    description = models.CharField(max_length=255)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    enregistre_par = models.ForeignKey(
        Utilisateur, on_delete=models.PROTECT, related_name='depenses'
    )
    note = models.TextField(blank=True, null=True)
    date_depense = models.DateTimeField(auto_now_add=True)
    synced = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Dépense'
        verbose_name_plural = 'Dépenses'
        ordering = ['-date_depense']

    def __str__(self):
        return f"{self.get_categorie_display()} – {self.montant} FCFA"
