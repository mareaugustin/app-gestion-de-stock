"""
Module: admin.py

Configurations de l'administration Django pour gérer les catégories, les articles et les livraisons.

Ce module définit les classes d'administration suivantes :

CategoryAdmin : Configuration pour le modèle Category dans l'interface d'administration.
ItemAdmin : Configuration pour le modèle Item dans l'interface d'administration.
DeliveryAdmin : Configuration pour le modèle Delivery dans l'interface d'administration.
"""

from django.contrib import admin
from .models import Category, Item, Delivery


class CategoryAdmin(admin.ModelAdmin):
    """
    Configuration de l'administration pour le modèle Categorie.
    """
    list_display = ('nom', 'slug')
    search_fields = ('nom',)
    ordering = ('nom',)


class ItemAdmin(admin.ModelAdmin):
    """
    Configuration de l'administration pour le modèle Article.
    """
    list_display = (
        'nom', 'categorie', 'quantite', 'prix', 'date_expiration', 'fournisseur'
    )
    search_fields = ('nom', 'nom__categorie', 'nom__fournisseur')
    list_filter = ('categorie', 'fournisseur')
    ordering = ('nom',)


class DeliveryAdmin(admin.ModelAdmin):
    """
    Configuration de l'administration pour le modèle Livraison.
    """
    list_display = (
        'article', 'nom_client', 'numero_telephone',
        'localisation', 'date', 'est_livré'
    )
    search_fields = ('nom__article', 'nom_client')
    list_filter = ('est_livré', 'date')
    ordering = ('-date',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Delivery, DeliveryAdmin)
