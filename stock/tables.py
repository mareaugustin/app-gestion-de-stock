import django_tables2 as tables
from .models import Item, Delivery, History


class ItemTable(tables.Table):
    """
    Représentation sous forme de table pour le modèle Article.
    """
    class Meta:
        model = Item
        template_name = "django_tables2/semantic.html"
        fields = (
            'id', 'nom', 'categorie', 'quantite',
            'prix_de_vente', 'date_expiration', 'fournisseur',
        )
        order_by_field = 'sort'




class HistoryTable(tables.Table):
    """
    Représentation sous forme de table pour le modèle Historique.
    """
    class Meta:
        model = History
        template_name = "django_tables2/semantic.html"
        fields = (
            'id', 'details', 'utilisateur', 'date'
        )
        order_by_field = 'sort'
        
        
        
        

class DeliveryTable(tables.Table):
    """
    Représentation sous forme de table pour le modèle Livraison.
    """
    class Meta:
        model = Delivery
        fields = (
            'id', 'article', 'nom_client', 'numero_telephone',
            'localisation', 'date', 'est_livré'
        )
