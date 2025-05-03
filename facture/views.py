# Django core imports
from django.urls import reverse

# Authentication et permissions
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Class basé sur les vues
from django.views.generic import (
    DetailView, CreateView, UpdateView, DeleteView
)

# Packages tiers
from django_tables2 import SingleTableView
from django_tables2.export.views import ExportMixin

# Importations des applications locales
from .models import Facture
from .tables import FactureTable


class FactureListView(LoginRequiredMixin, ExportMixin, SingleTableView):
    """
    Vue pour lister les factures avec une fonctionnalité d'exportation de tableau.
    """
    model = Facture
    table_class = FactureTable
    template_name = 'facture/facturelist.html'
    context_object_name = 'factures'
    paginate_by = 10
    table_pagination = False  


class FactureDetailView(DetailView):
    """
    Vue pour afficher les détails d'une facture.
    """
    model = Facture
    template_name = 'facture/facturedetail.html'

    def get_success_url(self):
        """
        Renvoie l'URL vers laquelle rediriger après une action réussie..
        """
        return reverse('facture-detail', kwargs={'slug': self.object.pk})


class FactureCreateView(LoginRequiredMixin, CreateView):
    """
    Vue pour créer une nouvelle facture.
    """
    model = Facture
    template_name = 'facture/facturecreate.html'
    fields = [
        'nom_client', 'numero_telephone', 'article',
        'prix_unitaire', 'quantite', 'livraison'
    ]

    def get_success_url(self):
        """
        Renvoie l'URL vers laquelle rediriger après une creation réussie..
        """
        return reverse('facturelist')


class FactureUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View for updating an existing facture.
    """
    model = Facture
    template_name = 'facture/factureupdate.html'
    fields = [
        'nom_client', 'numero_telephone', 'article',
        'prix_unitaire', 'quantite', 'livraison'
    ]

    def get_success_url(self):
        """
        Renvoie l'URL vers laquelle rediriger après une MAJ réussie..
        """
        return reverse('facturelist')

    def test_func(self):
        """
        Détermine si l'utilisateur a la permission de mettre à jour la facture.
        """
        return self.request.user.is_superuser


class FactureDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Vue pour supprimer une facture.
    """
    model = Facture
    template_name = 'facture/facturedelete.html'
    success_url = '/products'  

    def get_success_url(self):
        """
        Renvoie l'URL vers laquelle rediriger après une suppression réussie.
        """
        return reverse('facturelist')

    def test_func(self):
        """
        Détermine si l'utilisateur a la permission de supprimer la facture.
        """
        return self.request.user.is_superuser
