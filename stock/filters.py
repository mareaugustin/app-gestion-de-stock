import django_filters
from .models import Item


class ProductFilter(django_filters.FilterSet):
    """
Ensemble de filtres pour le modèle Item (Article).
    """
    class Meta:
        model = Item
        fields = ['nom', 'categorie', 'fournisseur']
