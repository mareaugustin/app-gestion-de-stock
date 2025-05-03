import django_tables2 as tables
from .models import Facture

class FactureTable(tables.Table):
    """
    Representation de la table pour le modele facture.
    """

    class Meta:
        model = Facture
        template_name = "django_tables2/semantic.html"
        fields = (
            'date', 'nom_client', 'numero_telephone', 'article',
            'prix_unitaire', 'quantite', 'total'
        )
        order_by = 'date'
