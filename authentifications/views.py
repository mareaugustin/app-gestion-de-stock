# Django core imports
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# Authentication et permissions
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Class basés sur les vues
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)

# Packages tiers
from django_tables2 import SingleTableView
from django_tables2.export.views import ExportMixin

# Importations des applications locales
from .models import Profile, Customer, Vendor
from .forms import (
    CreateUserForm, UserUpdateForm,
    ProfileUpdateForm, CustomerForm,
    VendorForm
)
from .tables import ProfileTable


def register(request):
    """
    Gère l'enregistrement des utilisateurs.
    Si la requête est de type POST, traite les données du formulaire pour créer un nouvel utilisateur.
    Redirige vers la page de connexion en cas d'enregistrement réussi.
    Pour les requêtes GET, affiche le formulaire d'enregistrement.
    """
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user-login')
    else:
        form = CreateUserForm()

    return render(request, 'authentifications/register.html', {'form': form})


@login_required
def profile(request):
    """
    Affiche la page du profil utilisateur.
    Nécessite que l'utilisateur soit connecté.
    """
    return render(request, 'authentifications/profile.html')


@login_required
def profile_update(request):
    """
    Gère la mise à jour du profil.
    Si la requête est de type POST, traite les données du formulaire pour mettre à jour les informations de l'utilisateur et du profil.
    Redirige vers la page du profil en cas de succès.
    Pour les requêtes GET, affiche les formulaires de mise à jour.
    """
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('user-profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(
        request,
        'authentifications/profile_update.html',
        {'u_form': u_form, 'p_form': p_form}
    )


class ProfileListView(LoginRequiredMixin, ExportMixin, SingleTableView):
    """
    Affiche une liste de profils sous forme de tableau.
    Nécessite que l'utilisateur soit connecté.
    Prend en charge l'exportation des données du tableau.
    La pagination est appliquée avec 10 profils par page.
    """
    model = Profile
    template_name = 'authentifications/stafflist.html'
    context_object_name = 'profiles'
    table_class = ProfileTable
    paginate_by = 10
    table_pagination = False


class ProfileCreateView(LoginRequiredMixin, CreateView):
    """
    Crée un nouveau profil.
    Nécessite que l'utilisateur soit connecté et ait le statut de superutilisateur.
    Redirige vers la liste des profils après une création réussie.
    """
    model = Profile
    template_name = 'authentifications/staffcreate.html'
    fields = ['user', 'role', 'statut']

    def get_success_url(self):
        """
        Renvoie l'URL vers laquelle rediriger après la création réussie d'un profil.
        """
        return reverse('profile_list')

    def test_func(self):
        """
        CVérifie si l"utilisateur est un superutilisateur
        """
        return self.request.user.is_superuser


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Met à jour un profil existant.
    Nécessite que l'utilisateur soit connecté et ait le statut de superutilisateur.
    Redirige vers la liste des profils après une mise à jour réussie.
    """
    model = Profile
    template_name = 'authentifications/staffupdate.html'
    fields = ['user', 'role', 'statut']

    def get_success_url(self):
        """
        Return the URL to redirect to after successfully updating a profile.
        """
        return reverse('profile_list')

    def test_func(self):
        """
        Check if the user is a superuser.
        """
        return self.request.user.is_superuser


class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
   Supprimer un profil existant.
    Nécessite que l'utilisateur soit connecté et ait le statut de superutilisateur.
    Redirige vers la liste des profils après une mise à jour réussie.
    """
    model = Profile
    template_name = 'authentifications/staffdelete.html'

    def get_success_url(self):
        return reverse('profile_list')

    def test_func(self):
        return self.request.user.is_superuser


class CustomerListView(LoginRequiredMixin, ListView):
    """
    Vue pour lister tous les clients.
    Nécessite que l'utilisateur soit connecté. Affiche une liste de tous les objets Customer
    """
    model = Customer
    template_name = 'authentifications/customer_list.html'
    context_object_name = 'customers'


class CustomerCreateView(LoginRequiredMixin, CreateView):
    """
    Vue pour créer un nouveau client.
    Nécessite que l'utilisateur soit connecté.
    Fournit un formulaire pour créer un nouvel objet Customer.
    En cas de soumission réussie du formulaire, redirige vers la liste des clients.
    """
    model = Customer
    template_name = 'authentifications/customer_form.html'
    form_class = CustomerForm
    success_url = reverse_lazy('customer_list')


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    """
    Vue pour modifier un nouveau client.
    Nécessite que l'utilisateur soit connecté.
    Fournit un formulaire pour créer un nouvel objet Customer.
    En cas de soumission réussie du formulaire, redirige vers la liste des clients.
    """
    model = Customer
    template_name = 'authentifications/customer_form.html'
    form_class = CustomerForm
    success_url = reverse_lazy('customer_list')


class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    """
   Vue pour supprimer un nouveau client.
    Nécessite que l'utilisateur soit connecté.
    Fournit un formulaire pour créer un nouvel objet Customer.
    En cas de soumission réussie du formulaire, redirige vers la liste des clients.
    """
    model = Customer
    template_name = 'authentifications/customer_confirm_delete.html'
    success_url = reverse_lazy('customer_list')


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@csrf_exempt
@require_POST
@login_required
def get_customers(request):
    if is_ajax(request) and request.method == 'POST':
        term = request.POST.get('term', '')
        customers = Customer.objects.filter(
            name__icontains=term
        ).values('id', 'name')
        customer_list = list(customers)
        return JsonResponse(customer_list, safe=False)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


class VendorListView(LoginRequiredMixin, ListView):
    model = Vendor
    template_name = 'authentifications/vendor_list.html'
    context_object_name = 'vendors'
    paginate_by = 10


class VendorCreateView(LoginRequiredMixin, CreateView):
    model = Vendor
    form_class = VendorForm
    template_name = 'authentifications/vendor_form.html'
    success_url = reverse_lazy('vendor-list')


class VendorUpdateView(LoginRequiredMixin, UpdateView):
    model = Vendor
    form_class = VendorForm
    template_name = 'authentifications/vendor_form.html'
    success_url = reverse_lazy('vendor-list')


class VendorDeleteView(LoginRequiredMixin, DeleteView):
    model = Vendor
    template_name = 'authentifications/vendor_confirm_delete.html'
    success_url = reverse_lazy('vendor-list')
