from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile, Customer, Vendor


class CreateUserForm(UserCreationForm):
    """Formulaire pour la création d'un nouvel utilisateur avec un champ email."""
    email = forms.EmailField()

    class Meta:
        """Meta options pour la class."""
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_superuser = True  # Définit l'utilisateur comme superutilisateur
        user.is_staff = True  # Définit l'utilisateur comme membre du personnel
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    """Formulaire pour la MAJ existante d'information d'un utilisateur."""
    class Meta:
        """Meta options pour la class."""
        model = User
        fields = [
            'username',
            'email'
        ]


class ProfileUpdateForm(forms.ModelForm):
    """Formulaire pour la MAJ d'information d'un profil d'un utilisateur."""
    class Meta:
        """Meta options pour la class."""
        model = Profile
        fields = [
            'telephone',
            'email',
            'prenom',
            'nom',
            'photo_profil',
        ]


class CustomerForm(forms.ModelForm):
    """Formulaire pour la création/modification de l'information d'un client"""
    class Meta:
        model = Customer
        fields = [
            'prenom',
            'nom',
            'addresse',
            'email',
            'phone',
            'point_fidelite',
        ]
        widgets = {
            'prenom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrer son prénom'
            }),
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrer son nom'
            }),
            'addresse': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Entrer son adresse',
                'rows': 3
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter son email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter son numéro de téléphone'
            }),
            'point_fidelite': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrer son point de fidélité'
            }),
        }


class VendorForm(forms.ModelForm):
    """Formulaire pour la création/modification de l'information d'un fournisseur."""
    class Meta:
        model = Vendor
        fields = ['nom', 'numero_phone', 'addresse']
        widgets = {
            'nom': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Nom du fournisseur'}
            ),
            'numero_phone': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Numéro de téléphone'}
            ),
            'addresse': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Adresse du fournisseur'}
            ),
        }
