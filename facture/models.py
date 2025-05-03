from django.db import models
from django_extensions.db.fields import AutoSlugField

from stock.models import Item


class Facture(models.Model):
    """
    Représente une facture pour un article acheté.
    
    Attributs :
    slug (str) : Slug unique basé sur la date.
    date (datetime) : Date de création de la facture.
    customer_name (str) : Nom du client.
    contact_number (str) : Numéro de contact du client.
    item (ForeignKey) : L'article facturé.
    price_per_item (float) : Prix par article.
    quantity (float) : Nombre d'articles achetés.
    shipping (float) : Frais de livraison.
    total (float) : Total avant les frais de livraison.
    grand_total (float) : Total incluant les frais de livraison.
    """

    slug = AutoSlugField(unique=True, populate_from='date')
    date = models.DateTimeField(
        auto_now=True,
        verbose_name='Date (e.g., 2022/11/22)'
    )
    nom_client = models.CharField(max_length=30)
    numero_telephone = models.CharField(max_length=13)
    article = models.ForeignKey(Item, on_delete=models.CASCADE)
    prix_unitaire = models.FloatField(verbose_name='Prix (Fcfa)')
    quantite = models.FloatField(default=0.00)
    livraison = models.FloatField(verbose_name='Frais de livraison (Fcfa)')
    total = models.FloatField(
        verbose_name='total (Fcfa)', editable=False
    )
    total_global = models.FloatField(
        verbose_name='Montant a payé (Fcfa)', editable=False
    )

    def save(self, *args, **kwargs):
        """
        Met à jour les champs total et grand_total avant l'enregistrement.
        """
        self.total = round(self.quantite * self.prix_unitaire, 2)
        self.total_global = round(self.total + self.livraison, 2)
        return super().save(*args, **kwargs)

    def __str__(self):
        """
        Return le slug de la facture.
        """
        return self.slug
    
    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
