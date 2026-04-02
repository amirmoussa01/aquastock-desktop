from django.db import models
import uuid


class Categorie(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'
        ordering = ['nom']

    def __str__(self):
        return self.nom


class Produit(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.PROTECT,
        related_name='produits'
    )
    nom = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    prix_achat = models.DecimalField(max_digits=10, decimal_places=2)
    prix_vente = models.DecimalField(max_digits=10, decimal_places=2)
    stock_actuel = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    seuil_alerte = models.DecimalField(
        max_digits=10, decimal_places=2, default=5
    )
    unite = models.CharField(max_length=20, default='kg')
    image = models.ImageField(
        upload_to='produits/', blank=True, null=True
    )
    est_actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Produit'
        verbose_name_plural = 'Produits'
        ordering = ['nom']

    def __str__(self):
        return f"{self.nom} ({self.stock_actuel} {self.unite})"

    def stock_faible(self):
        return self.stock_actuel <= self.seuil_alerte

    def benefice_unitaire(self):
        return self.prix_vente - self.prix_achat

