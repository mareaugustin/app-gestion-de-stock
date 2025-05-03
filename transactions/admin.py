from django.contrib import admin
from .models import Sale, SaleDetail, Purchase


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface d'administration pour le modèle Vente.
    """
    list_display = (
        'id',
        'client',
        'date_ajout',
        'total_global',
        'montant_paye',
        'montant_change'
    )
    search_fields = ('nom__client', 'id')
    list_filter = ('date_ajout', 'client')
    ordering = ('-date_ajout',)
    readonly_fields = ('date_ajout',)
    date_hierarchy = 'date_ajout'

    def save_model(self, request, obj, form, change):
        """
        SEnregistre l'instance Sale en remplaçant le comportement par défaut de la méthode save.
        """
        super().save_model(request, obj, form, change)


@admin.register(SaleDetail)
class SaleDetailAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface d'administration pour le modèle Detail de vente.
    """
    list_display = (
        'id',
        'vente',
        'article',
        'prix',
        'quantite',
        'detail_total'
    )
    search_fields = ('vente__id', 'article__nom')
    list_filter = ('vente', 'article')
    ordering = ('vente', 'article')

    def save_model(self, request, obj, form, change):
        """
        Enregistre l'instance SaleDetail en remplaçant le comportement par défaut de la méthode save.
        """
        super().save_model(request, obj, form, change)


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface d'administration pour le modèle Achat.
    """
    list_display = (
        'slug',
        'article',
        'fournisseur',
        'order_date',
        'date_livraison',
        'quantite',
        'prix',
        'valeur_total',
        'statut_livraison',
    )
    search_fields = ('article__nom', 'fournisseur__nom', 'slug')
    list_filter = ('order_date', 'fournisseur', 'statut_livraison')
    ordering = ('-order_date',)
    readonly_fields = ('valeur_total',)

    def save_model(self, request, obj, form, change):
        """
        Enregistre l'instance Achat et calcule la valeur totale.
        """
        obj.valeur_total = obj.prix * obj.quantite
        super().save_model(request, obj, form, change)
