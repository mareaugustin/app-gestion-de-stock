from django.contrib import admin
from .models import Facture

@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface d'administration pour le modèle Facture.
    """
    fields = (
        'nom_client', 'numero_telephone', 'article',
        'prix_unitaire', 'quantite'
    )
    list_display = (
        'date', 'nom_client', 'numero_telephone', 'article',
        'prix_unitaire', 'quantite', 'livraison', 'total',
        'total_global'
    )
