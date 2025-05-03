from django.db import models
from django_extensions.db.fields import AutoSlugField

from stock.models import Item
from authentifications.models import Vendor, Customer

DELIVERY_CHOICES = [("A", "En attente"), ("S", "Réussie")]


class Sale(models.Model):
    """
    Représente une transaction de vente impliquant un client.
    """

    date_ajout = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de vente",
    )
    client = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        db_column="client",
    )
    sous_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.0
    )
    total_global = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.0
    )
    montant_taxe = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.0,
        null=True, blank=True
    )
    pourcentage_taxe = models.FloatField(default=0.0, null=True, blank=True)
    montant_paye = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.0
    )
    montant_change = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.0
    )

    class Meta:
        db_table = "sales"
        verbose_name = "Vente"
        verbose_name_plural = "Ventes"

    def __str__(self):
        """
        Renvoie une représentation sous forme de chaîne de l'instance Sale.
        """
        return (
            f"Vente ID: {self.id} | "
            f"Total global: {self.total_global} | "
            f"Date: {self.date_ajout}"
        )

    def sum_products(self):
        """
        Renvoie la quantité totale de produits dans la vente.
        """
        return sum(detail.quantite for detail in self.saledetail_set.all())


class SaleDetail(models.Model):
    """
    Représente les détails d'une vente spécifique, y compris l'article et la quantité.
    """

    vente = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        db_column="vente",
        related_name="saledetail_set"
    )
    article = models.ForeignKey(
        Item,
        on_delete=models.DO_NOTHING,
        db_column="article"
    )
    prix = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    quantite = models.PositiveIntegerField()
    detail_total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "sale_details"
        verbose_name = "Detail de vente"
        verbose_name_plural = "Details de vente"

    def __str__(self):
        """
        Renvoie une représentation sous forme de chaîne de l'instance SaleDetail.
        """
        return (
            f"Detail ID: {self.id} | "
            f"Vente ID: {self.vente.id} | "
            f"Quantité: {self.quantite}"
        )


class Purchase(models.Model):
    """
    Représente l'achat d'un article, y compris les détails 
    du fournisseur et le statut de livraison.
    """

    slug = AutoSlugField(unique=True, populate_from="fournisseur")
    article = models.ForeignKey(Item, on_delete=models.CASCADE)
    description = models.TextField(max_length=300, blank=True, null=True)
    fournisseur = models.ForeignKey(
        Vendor, related_name="achats", on_delete=models.CASCADE
    )
    order_date = models.DateTimeField(auto_now_add=True)
    date_livraison = models.DateTimeField(
        blank=True, null=True, verbose_name="Date de livraison"
    )
    quantite = models.PositiveIntegerField(default=0)
    statut_livraison = models.CharField(
        choices=DELIVERY_CHOICES,
        max_length=1,
        default="A",
        verbose_name="Statut de livraison",
    )
    prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.0,
        verbose_name="Prix d'achat (FCFA)",
    )
    valeur_total = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        """
        Calcule la valeur totale avant d'enregistrer l'instance Purchase.
        """
        self.valeur_total = self.prix * self.quantite
        super().save(*args, **kwargs)
        # Update the item quantity
        self.article.quantite += self.quantite - self.quantite
        self.article.save()

    def __str__(self):
        """
       Renvoie une représentation sous forme de chaîne de l'instance Purchase.
        """
        return str(self.article.nom)

    class Meta:
        verbose_name = "Achat"
        verbose_name_plural = "Achats"
        ordering = ["order_date"]
