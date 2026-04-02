from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class Utilisateur(AbstractUser):

    ROLES = (
        ('admin', 'Administrateur'),
        ('gestionnaire', 'Gestionnaire'),
        ('vendeur', 'Vendeur'),
    )

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    role = models.CharField(
        max_length=20, choices=ROLES, default='vendeur'
    )
    telephone = models.CharField(
        max_length=20, blank=True, null=True
    )
    est_actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

    def est_admin(self):
        return self.role == 'admin'

    def est_gestionnaire(self):
        return self.role == 'gestionnaire'

    def est_vendeur(self):
        return self.role == 'vendeur'

    def save(self, *args, **kwargs):
        if self.is_superuser and self.role != 'admin':
            self.role = 'admin'
        super().save(*args, **kwargs)
