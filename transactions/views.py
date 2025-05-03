# Standard library imports
import json
import logging

# Django core imports
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.shortcuts import render
from django.db import transaction

# Class-based views
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Authentication and permissions
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Third-party packages
from openpyxl import Workbook

# Local app imports
from stock.models import Item
from authentifications.models import Customer
from .models import Sale, Purchase, SaleDetail
from .forms import PurchaseForm


logger = logging.getLogger(__name__)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def export_sales_to_excel(request):
    # Créez un classeur et sélectionnez la feuille de calcul active
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Ventes'

    # Définir les en-têtes de colonnes
    columns = [
        'ID', 'Date', 'Client', 'Sous total',
        'Total global', 'Montant taxe', 'Taxe (%)',
        'Montant payé', 'Reste'
    ]
    worksheet.append(columns)

    # Récupérer les données de ventes.
    sales = Sale.objects.all()

    for sale in sales:
        if sale.date_ajout.tzinfo is not None:
            date_ajout = sale.date_ajout.replace(tzinfo=None)
        else:
            date_ajout = sale.date_ajout

        worksheet.append([
            sale.id,
            date_ajout,
            sale.client.phone,
            sale.sous_total,
            sale.total_global,
            sale.montant_taxe,
            sale.pourcentage_taxe,
            sale.montant_paye,
            sale.montant_change
        ])

    # Configurer la réponse pour envoyer le fichier.
    response = HttpResponse(
        content_type=(
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    )
    response['Content-Disposition'] = 'attachment; filename=Tableau de Ventes.csv'
    workbook.save(response)

    return response


def export_purchases_to_excel(request):
    # Créez un classeur et sélectionnez la feuille de calcul active.
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Achats'

    # Definir les en-têtes de colonnes
    columns = [
        'ID', 'Article', 'Description', 'Fournisseur', 'Date de commande',
        'Date de livraison', 'Quantite', 'Statut de livraison',
        'Prix unitaire (Fcfa)', 'Valeur totale'
    ]
    worksheet.append(columns)

    # Récupérer les données d'achats.
    purchases = Purchase.objects.all()

    for purchase in purchases:
        # Vérifiez si les dates sont nulles
        date_livraison = purchase.date_livraison
        order_date = purchase.order_date

        if date_livraison is not None and date_livraison.tzinfo is not None:
            date_livraison = date_livraison.replace(tzinfo=None)

        if order_date is not None and order_date.tzinfo is not None:
            order_date = order_date.replace(tzinfo=None)

        worksheet.append([
            purchase.id,
            purchase.article.nom if purchase.article else "N/A",
            purchase.description,
            purchase.fournisseur.nom if purchase.fournisseur else "N/A",
            order_date,
            date_livraison,
            purchase.quantite,
            purchase.get_statut_livraison_display(),
            purchase.prix,
            purchase.valeur_total
        ])

    # Set up the response to send the file
    response = HttpResponse(
        content_type=(
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    )
    response['Content-Disposition'] = 'attachment; filename=Achats.csv'
    workbook.save(response)

    return response


class SaleListView(LoginRequiredMixin, ListView):
    """
    Vue pour lister toutes les ventes avec pagination.
    """

    model = Sale
    template_name = "transactions/sales_list.html"
    context_object_name = "ventes"
    paginate_by = 10
    ordering = ['date_ajout']


class SaleDetailView(LoginRequiredMixin, DetailView):
    """
    Vue pour afficher les détails d'une vente spécifique.
    """

    model = Sale
    template_name = "transactions/saledetail.html"


def SaleCreateView(request):
    context = {
        "active_icon": "ventes",
        "clients": [c.to_select2() for c in Customer.objects.all()]
    }

    if request.method == 'POST':
        if is_ajax(request=request):
            try:
                # Charger les données JSON depuis le corps de la requête.
                data = json.loads(request.body)
                logger.info(f"Données reçues: {data}")

                # Valider les champs requis
                required_fields = [
                    'client', 'sous_total', 'total_global',
                    'montant_paye', 'montant_change', 'articles'
                ]
                for field in required_fields:
                    if field not in data:
                        raise ValueError(f"Champ obligatoire manquant: {field}")

                # Creer les attributs de la vente
                sale_attributes = {
                    "client": Customer.objects.get(id=int(data['client'])),
                    "sous_total": float(data["sous_total"]),
                    "total_global": float(data["total_global"]),
                    "montant_taxe": float(data.get("montant_taxe", 0.0)),
                    "pourcentage_taxe": float(data.get("pourcentage_taxe", 0.0)),
                    "montant_paye": float(data["montant_paye"]),
                    "montant_change": float(data["montant_change"]),
                }

                # Utiliser une transaction pour garantir l'atomicité.
                with transaction.atomic():
                    # Create the sale
                    new_sale = Sale.objects.create(**sale_attributes)
                    logger.info(f"Vente créée: {new_sale}")

                    # Créer une vente et mettre à jour la quantité des articles
                    items = data["articles"]
                    if not isinstance(items, list):
                        raise ValueError("Les articles doivent être une liste")

                    for item in items:
                        if not all(
                            k in item for k in [
                                "id", "prix", "quantite", "article_total"
                            ]
                        ):
                            raise ValueError("Il manque des champs obligatoires pour l'article")

                        item_instance = Item.objects.get(id=int(item["id"]))
                        if item_instance.quantite < int(item["quantite"]):
                            raise ValueError(f"Pas assez de stock pour vendrel'article: {item_instance.nom}")

                        detail_attributes = {
                            "vente": new_sale,
                            "article": item_instance,
                            "prix": float(item["prix"]),
                            "quantite": int(item["quantite"]),
                            "detail_total": float(item["article_total"])
                        }
                        SaleDetail.objects.create(**detail_attributes)
                        logger.info(f"Détail de la vente créé: {detail_attributes}")

                        # Reduce item quantity
                        item_instance.quantite -= int(item["quantite"])
                        item_instance.save()

                return JsonResponse(
                    {
                        'status': 'succès',
                        'message': f'L\'article {item_instance.nom} a été vendu avec succès!',
                        'redirect': '/transactions/sales/'
                    }
                )

            except json.JSONDecodeError:
                return JsonResponse(
                    {
                        'status': 'erreur',
                        'message': 'Format JSON invalide dans le corps de la requête!'
                    }, status=400)
            except Customer.DoesNotExist:
                return JsonResponse({
                    'status': 'erreur',
                    'message': 'Le client n\'existe pas!'
                    }, status=400)
            except Item.DoesNotExist:
                return JsonResponse({
                    'status': 'erreur',
                    'message': 'L\'article n\'existe pas!'
                    }, status=400)
            except ValueError as ve:
                return JsonResponse({
                    'status': 'erreur',
                    'message': f'Value error: {str(ve)}'
                    }, status=400)
            except TypeError as te:
                return JsonResponse({
                    'status': 'erreur',
                    'message': f'Type error: {str(te)}'
                    }, status=400)
            except Exception as e:
                logger.error(f"Exception lors de la création d'une vente: {e}")
                return JsonResponse(
                    {
                        'status': 'erreur',
                        'message': (
                            f'Il y a eu une erreur lors de la création: {str(e)}'
                        )
                    }, status=500)

    return render(request, "transactions/sale_create.html", context=context)


class SaleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    LA vue pour supprimer une vente.
    """

    model = Sale
    template_name = "transactions/saledelete.html"

    def get_success_url(self):
        """
        Redirection à la liste des ventes après une suppression réussie.
        """
        return reverse("saleslist")

    def test_func(self):
        """
        Autoriser la suppression uniquement pour les superutilisateurs.
        """
        return self.request.user.is_superuser


class PurchaseListView(LoginRequiredMixin, ListView):
    """
    Vue pour lister tous les achats avec pagination.
    """

    model = Purchase
    template_name = "transactions/purchases_list.html"
    context_object_name = "purchases"
    paginate_by = 10


class PurchaseDetailView(LoginRequiredMixin, DetailView):
    """
    Vue pour afficher les détails d'un achat spécifique.
    """

    model = Purchase
    template_name = "transactions/purchasedetail.html"


class PurchaseCreateView(LoginRequiredMixin, CreateView):
    """
    Vue pour creer un nouvel achat.
    """

    model = Purchase
    form_class = PurchaseForm
    template_name = "transactions/purchases_form.html"

    def get_success_url(self):
        """
        Redirection à la liste des achats après une soumission réussie du formulaire.
        """
        return reverse("purchaseslist")


class PurchaseUpdateView(LoginRequiredMixin, UpdateView):
    """
    Vue pour mettre à jour un achat existant.
    """

    model = Purchase
    form_class = PurchaseForm
    template_name = "transactions/purchases_form.html"

    def get_success_url(self):
        """
        Redirection à la liste des achats après une mise à jour réussie du formulaire.
        """
        return reverse("purchaseslist")


class PurchaseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Vue pour supprimer un achat.
    """

    model = Purchase
    template_name = "transactions/purchasedelete.html"

    def get_success_url(self):
        """
        Redirection à la liste des achats après une suppression réussie.
        """
        return reverse("purchaseslist")

    def test_func(self):
        """
        Autoriser la suppression uniquement pour les superutilisateurs.
        """
        return self.request.user.is_superuser
