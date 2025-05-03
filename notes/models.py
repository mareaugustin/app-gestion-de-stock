from django.db import models
from autoslug import AutoSlugField


class Note(models.Model):
    """Modèle représentant une note avec divers détails et un statut de paiement."""

    slug = AutoSlugField(unique=True, populate_from='date')
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date (e.g., 2022/11/22)'
    )
    entreprise_nom = models.CharField(
        max_length=30,
        blank=False,
        null=False,
        help_text='Nom de l\'entreprise'
    )
    numero_telephone = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text='Numero de téléphone de l\'entreprise'
    )
    email = models.EmailField(
        blank=True,
        null=True,
        help_text='Adresse email de l\'entreprise'
    )
    addresse = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text='Addresse de l\'entreprise'
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text='Pourquoi s\'approvisionner ?'
    )
    paiement_details = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        help_text='Details de paiement'
    )
    montant = models.FloatField(
        verbose_name='Montant en (FCFA)',
        help_text='Montant total de la facture',
    )
    statut = models.BooleanField(
        default=False,
        verbose_name='Payé',
        help_text='Statut de paiement de la facture'
    )

    def __str__(self):
        return self.entreprise_nom