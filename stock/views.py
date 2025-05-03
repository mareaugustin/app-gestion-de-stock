"""
Module: stock.views

Contient les vues Django pour gérer les articles, les profils et
les livraisons dans l'application de gestion de stock.

Les classes gèrent la liste des produits, leur création, mise à jour, 
suppression et la gestion des livraisons.
Le module s'intègre aux fonctionnalités d'authentification
et de requêtes de Django.
"""

# Standard library imports
import operator
from functools import reduce

# Django core imports
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Count, Sum

# Authentication et permissions
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Class-based views
from django.views.generic import (
    DetailView, CreateView, UpdateView, DeleteView, ListView
)
from django.views.generic.edit import FormMixin

# Third-party packages
from django_tables2 import SingleTableView
import django_tables2 as tables
from django_tables2.export.views import ExportMixin

# Local app imports
from authentifications.models import Profile, Vendor
from transactions.models import Sale
from .models import Category, Item, Delivery, History
from .forms import ItemForm, CategoryForm, DeliveryForm
from .tables import ItemTable, HistoryTable

from django.contrib import messages #pour recevoir les notifs sur notre dashboard

# @login_required
def dashboard(request):
    """
    Vue pour afficher le tableau de bord.
    Accessible à tous les utilisateurs, mais les actions sont limitées pour les non-connectés.
    """
    profiles = Profile.objects.all()
    Category.objects.annotate(nitem=Count("item"))
    items = Item.objects.all()
    total_items = (
        Item.objects.all()
        .aggregate(Sum("quantite"))
        .get("quantite__sum", 0.00)
    )
    items_count = items.count()
    profiles_count = profiles.count()
    
     # Produits avec un stock faible
    low_stock_items = items.filter(quantite__lte=5)
    if low_stock_items.exists():
        message = "Les articles suivants ont un stock faible : " + ", ".join(
            [f"{item.nom} (Quantité : {item.quantite})" for item in low_stock_items]
        )
        messages.warning(request, message)

    # Preparation des données pour le graphique
    category_counts = Category.objects.annotate(
        item_count=Count("item")
    ).values("nom", "item_count")
    categories = [cat["nom"] for cat in category_counts]
    category_counts = [cat["item_count"] for cat in category_counts]

    sale_dates = (
        Sale.objects.values("date_ajout__date")
        .annotate(total_sales=Sum("total_global"))
        .order_by("date_ajout__date")
    )
    sale_dates_labels = [
        date["date_ajout__date"].strftime("%Y-%m-%d") for date in sale_dates
    ]
    sale_dates_values = [float(date["total_sales"]) for date in sale_dates]
    
    # Données pour le graphique des quantités des articles
    item_labels = [item.nom for item in items]  # Noms des articles
    item_quantities = [item.quantite for item in items]  # Quantités des articles
    item_colors = ['#FF0000' if item.quantite <= 5 else '#4BC0C0' for item in items]  # Rouge si quantité <= 5, sinon bleu

    context = {
        "items": items,
        "profiles": profiles,
        "profiles_count": profiles_count,
        "items_count": items_count,
        "total_items": total_items,
        
        "low_stock_items": low_stock_items,  # Ajout des produits avec un stock faible
        
        "fournisseurs": Vendor.objects.all(),
        "livraison": Delivery.objects.all(),
        "sale": Sale.objects.all(),
        "categories": categories,
        "categorie_counts": category_counts,
        "sale_dates_labels": sale_dates_labels,
        "sale_dates_values": sale_dates_values,
        
        "item_labels": item_labels,
        "item_quantities": item_quantities,
        "item_colors": item_colors,
        
        "can_edit": request.user.is_authenticated and request.user.is_superuser,  # Autorise les actions uniquement pour les superutilisateurs connectés
    }
    return render(request, "stock/dashboard.html", context)


class ProductListView(LoginRequiredMixin, ExportMixin, tables.SingleTableView):
    """
    Classe de vue pour afficher une liste de produits.

    Attributs :
    model : Le modèle associé à la vue.
    table_class : La classe de tableau utilisée pour le rendu.
    template_name : Le template HTML utilisé pour le rendu de la vue.
    context_object_name : Le nom de la variable pour l'objet de contexte.
    paginate_by : Nombre d'articles par page pour la pagination.
    """

    model = Item
    table_class = ItemTable
    template_name = "stock/productslist.html"
    context_object_name = "items"
    paginate_by = 10
    SingleTableView.table_pagination = False
    

# La vue des historiques
class HistoryListView(LoginRequiredMixin, ExportMixin, tables.SingleTableView):
    """
    Classe de vue pour afficher une liste des historiques.

    Attributs :
    model : Le modèle associé à la vue.
    table_class : La classe de tableau utilisée pour le rendu.
    template_name : Le template HTML utilisé pour le rendu de la vue.
    context_object_name : Le nom de la variable pour l'objet de contexte.
    paginate_by : Nombre d'articles par page pour la pagination.
    """

    model = History
    table_class = HistoryTable
    template_name = "stock/historylist.html"
    context_object_name = "histories"
    paginate_by = 10
    
    
class ItemSearchListView(ProductListView):
    """
    Classe de vue pour rechercher et afficher une liste filtrée d'articles.

    Attributs :
    paginate_by : Nombre d'articles par page pour la pagination.
    """

    paginate_by = 10

    def get_queryset(self):
        result = super(ItemSearchListView, self).get_queryset()

        query = self.request.GET.get("q")
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(
                    operator.and_, (Q(nom__icontains=q) for q in query_list)
                )
            )
        return result


class ProductDetailView(LoginRequiredMixin, FormMixin, DetailView):
    """
    Classe de vue pour afficher des informations détaillées sur un produit.

    Attributs :
    model : Le modèle associé à la vue.
    template_name : Le template HTML utilisé pour le rendu de la vue.
    """

    model = Item
    template_name = "stock/productdetail.html"

    def get_success_url(self):
        return reverse("product-detail", kwargs={"slug": self.object.slug})


class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    Classe de vue pour créer un nouveau produit.

    Attributs :
    model : Le modèle associé à la vue.
    template_name : Le template HTML utilisé pour le rendu de la vue.
    form_class : La classe de formulaire utilisée pour la saisie des données.
    success_url : L'URL vers laquelle rediriger après une soumission réussie du formulaire.
    """

    model = Item
    template_name = "stock/productcreate.html"
    form_class = ItemForm
    success_url = "/products"
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Enregistrer l'action dans l'historique
        History.objects.create(
            produit=self.object.nom,
            utilisateur=self.request.user,
            action='add',
            details=f"Produit {self.object.nom} a été ajouté par {self.request.user}.",
        )
        return response


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Classe de vue pour mettre à jour les informations d'un produit.

    Attributs :
    model : Le modèle associé à la vue.
    template_name : Le template HTML utilisé pour le rendu de la vue.
    form_class : La classe de formulaire utilisée pour la saisie des données.
    success_url : L'URL vers laquelle rediriger après une soumission réussie du formulaire.
    """

    model = Item
    template_name = "stock/productupdate.html"
    form_class = ItemForm
    success_url = "/products"
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Enregistrer l'action dans l'historique
        History.objects.create(
            produit=self.object.nom,
            utilisateur=self.request.user,
            action='update',
            details=f"Produit {self.object.nom} modifié par {self.request.user}.",
        )
        return response

    def test_func(self):
        return self.request.user.is_superuser



class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Classe de vue pour supprimer un produit.

    Attributs :
    model : Le modèle associé à la vue.
    template_name : Le template HTML utilisé pour le rendu de la vue.
    success_url : L'URL vers laquelle rediriger après une suppression réussie.
    """

    model = Item
    template_name = "stock/productdelete.html"
    success_url = "/products"
    
    def delete(self, request, *args, **kwargs,):
        product = self.get_object()
        # Enregistrer l'action dans l'historique
        History.objects.create(
            produit=product.nom,
            utilisateur=request.user,
            action='delete',
            details=f"Produit {product.nom} supprimé par {request.user}.",
        )
        return super().delete(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.is_superuser


class DeliveryListView(
    LoginRequiredMixin, ExportMixin, tables.SingleTableView
):
    """
    Classe de vue pour afficher une liste de livraisons.

    Attributs :
    model : Le modèle associé à la vue.
    pagination : Nombre d'articles par page pour la pagination.
    template_name : Le template HTML utilisé pour le rendu de la vue.
    context_object_name : Le nom de la variable pour l'objet de contexte.
    """

    model = Delivery
    pagination = 10
    template_name = "stock/deliveries.html"
    context_object_name = "deliveries"


class DeliverySearchListView(DeliveryListView):
    """
    Classe de vue pour rechercher et afficher une liste filtrée de livraisons.

    Attributs :
    paginate_by : Nombre d'articles par page pour la pagination.
    """

    paginate_by = 10

    def get_queryset(self):
        result = super(DeliverySearchListView, self).get_queryset()

        query = self.request.GET.get("q")
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(
                    operator.
                    and_, (Q(customer_name__icontains=q) for q in query_list)
                )
            )
        return result


class DeliveryDetailView(LoginRequiredMixin, DetailView):
    """
    Classe de vue pour afficher des informations détaillées sur une livraison.

    Attributs :
    model : Le modèle associé à la vue.
    template_name : Le template HTML utilisé pour le rendu de la vue.
    """

    model = Delivery
    template_name = "stock/deliverydetail.html"


class DeliveryCreateView(LoginRequiredMixin, CreateView):
    """
    Classe de vue pour créer une nouvelle livraison.

    Attributs :
    model : Le modèle associé à la vue.
    fields : Les champs à inclure dans le formulaire.
    template_name : Le template HTML utilisé pour le rendu de la vue.
    success_url : L'URL vers laquelle rediriger après une soumission réussie du formulaire.
    """

    model = Delivery
    form_class = DeliveryForm
    template_name = "stock/delivery_form.html"
    success_url = "/deliveries"


class DeliveryUpdateView(LoginRequiredMixin, UpdateView):
    """
    Classe de vue pour mettre à jour les informations de livraison.

    Attributs :
    model : Le modèle associé à la vue.
    fields : Les champs à mettre à jour.
    template_name : Le template HTML utilisé pour le rendu de la vue.
    success_url : L'URL vers laquelle rediriger après une soumission réussie du formulaire.
    """

    model = Delivery
    form_class = DeliveryForm
    template_name = "stock/delivery_form.html"
    success_url = "/deliveries"


class DeliveryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Classe de vue pour supprimer une livraison.

    Attributs :
    model : Le modèle associé à la vue.
    template_name : Le template HTML utilisé pour le rendu de la vue.
    success_url : L'URL vers laquelle rediriger après une suppression réussie.
    """

    model = Delivery
    template_name = "stock/deliverydelete.html"
    success_url = "/deliveries"

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:
            return False


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'stock/category_list.html'
    context_object_name = 'categories'
    paginate_by = 10
    login_url = 'login'


class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'stock/category_detail.html'
    context_object_name = 'category'
    login_url = 'login'


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'stock/category_form.html'
    form_class = CategoryForm
    login_url = 'login'

    def get_success_url(self):
        return reverse_lazy('category-detail', kwargs={'pk': self.object.pk})


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    template_name = 'stock/category_form.html'
    form_class = CategoryForm
    login_url = 'login'

    def get_success_url(self):
        return reverse_lazy('category-detail', kwargs={'pk': self.object.pk})


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'stock/category_confirm_delete.html'
    context_object_name = 'category'
    success_url = reverse_lazy('category-list')
    login_url = 'login'


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@csrf_exempt
@require_POST
@login_required
def get_items_ajax_view(request):
    if is_ajax(request):
        try:
            term = request.POST.get("term", "")
            data = []

            items = Item.objects.filter(nom__icontains=term)
            for item in items[:10]:
                data.append(item.to_json())

            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Not an AJAX request'}, status=400)
