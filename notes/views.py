# Django core imports
from django.urls import reverse

# Class bas" sur des vues génériques
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView
)

# Authentication et permissions
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Package tiers
from django_tables2 import SingleTableView
from django_tables2.export.views import ExportMixin

# Importations des app localess
from .models import Note
from .tables import NoteTable
from authentifications.models import Profile


class NoteListView(LoginRequiredMixin, ExportMixin, SingleTableView):
    """Vue pour lister les notes."""
    model = Note
    table_class = NoteTable
    template_name = 'notes/note_list.html'
    context_object_name = 'notes'
    paginate_by = 10
    SingleTableView.table_pagination = False


class NoteCreateView(LoginRequiredMixin, CreateView):
    """Vue pour créerr les notes.."""
    model = Note
    template_name = 'notes/notecreate.html'
    fields = [
        'entreprise_nom',
        'numero_telephone',
        'email',
        'addresse',
        'description',
        'paiement_details',
        'montant',
        'statut'
    ]

    def get_success_url(self):
        """Redirige vers la liste des notes après une mise à jour réussie."""
        return reverse('note_list')


class NoteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Vue pour MAJ les notes.."""
    model = Note
    template_name = 'notes/noteupdate.html'
    fields = [
        'entreprise_nom',
        'numero_telephone',
        'email',
        'addresse',
        'description',
        'paiement_details',
        'montant',
        'statut'
    ]

    def test_func(self):
        """Voir si l'utilisateur a les permissions requis."""
        return self.request.user.profile in Profile.objects.all()

    def get_success_url(self):
        """Redirige vers la liste des notes après une mise à jour réussie.."""
        return reverse('note_list')


class NoteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Vue pour supprimer la note."""
    model = Note
    template_name = 'notes/notedelete.html'

    def test_func(self):
        """Checker voir si l'utilisateur a les permissions requis."""
        return self.request.user.is_superuser

    def get_success_url(self):
        """Redirige vers la liste des notes après une suppression réussie."""
        return reverse('note_list')
