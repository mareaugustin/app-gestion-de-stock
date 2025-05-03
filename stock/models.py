"""
Module: models.py

Contient les modèles Django pour gérer les catégories, les articles et les livraisons.

Ce module définit les classes suivantes :

Category : Représente une catégorie pour les articles.
Item : Représente un article dans la gestion de stock.
Delivery : Représente une livraison d'un article à un client.
Chaque classe fournit des champs et des méthodes spécifiques pour gérer les données associées.
"""

from django.db import models
from django.urls import reverse
from django.forms import model_to_dict
from django_extensions.db.fields import AutoSlugField
from phonenumber_field.modelfields import PhoneNumberField
from authentifications.models import Vendor
from django.contrib.auth.models import User


class Category(models.Model):
    """
    Représente une catégorie pour les articles.
    """
    nom = models.CharField(max_length=50)
    slug = AutoSlugField(unique=True, populate_from='nom')

    def __str__(self):
        """
        Représentation sous forme de chaîne de la catégorie.
        """
        return f"{self.nom}"

    class Meta:
        verbose_name_plural = 'Categories'


class Item(models.Model):
    """
    Représente un article dans la gestion de stock.
    """
    slug = AutoSlugField(unique=True, populate_from='nom')
    nom = models.CharField(max_length=50)
    description = models.TextField(max_length=256)
    categorie = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantite = models.IntegerField(default=0)
    prix = models.FloatField(default=0)
    date_expiration = models.DateTimeField(null=True, blank=True)
    fournisseur = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """
        Représentation sous forme de chaîne l'article.
        """
        return (
            f"{self.nom} - Categorie: {self.categorie}, "
            f"Quantité: {self.quantite}"
        )

    def get_absolute_url(self):
        """
        Renvoie l'URL absolue pour la vue détaillée d'un article.
        """
        return reverse('item-detail', kwargs={'slug': self.slug})

    def to_json(self):
        product = model_to_dict(self)
        product['id'] = self.id
        product['text'] = self.nom
        product['categorie'] = self.categorie.nom
        product['quantite'] = 1
        product['total_items'] = 0
        return product

    class Meta:
        ordering = ['nom']
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        
        

class History(models.Model):
    ACTION_CHOICES = [
        ('add', 'Ajouté'),
        ('update', 'Modifié'),
        ('delete', 'Supprimé'),
    ]

    produit = models.CharField(max_length=255, blank=True, null=True)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.produit} {self.get_action_display()} par {self.utilisateur} le {self.date}"
    
    
    
class Delivery(models.Model):
    """
    Représente une livraison d'un article à un client.
    """
    article = models.ForeignKey(
        Item, blank=True, null=True, on_delete=models.SET_NULL
    )
    nom_client = models.CharField(max_length=30, blank=True, null=True)
    numero_telephone = PhoneNumberField(blank=True, null=True)
    localisation = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateTimeField()
    est_livré = models.BooleanField(
        default=False, verbose_name='Est livré'
    )

    def __str__(self):
        """
        Représentation sous forme de chaîne de la livraison.
        """
        return (
            f"Livraison de {self.article} à {self.nom_client} "
            f"au {self.localisation} le {self.date}"
        )
        
    class Meta:
        verbose_name = "Livraison"
        verbose_name_plural = "Livraisons"
