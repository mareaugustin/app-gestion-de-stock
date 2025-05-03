import django_tables2 as tables
from .models import Sale, Purchase


class SaleTable(tables.Table):
    class Meta:
        model = Sale
        template_name = "django_tables2/semantic.html"
        fields = (
            'article',
            'nom_client',
            'date_transaction',
            'methode_paiement',
            'quantite',
            'prix',
            'valeur_total',
            'montant_recu',
            'balance',
            'profile'
        )
        order_by_field = 'sort'


class PurchaseTable(tables.Table):
    class Meta:
        model = Purchase
        template_name = "django_tables2/semantic.html"
        fields = (
            'article',
            'fournisseur',
            'order_date',
            'date_livraison',
            'quantite',
            'statut_livraison',
            'prix',
            'valeur_total',
        )
        order_by_field = 'sort'
