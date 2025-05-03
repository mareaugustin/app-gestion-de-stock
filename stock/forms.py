from django import forms
from .models import Item, Category, Delivery


class ItemForm(forms.ModelForm):
    """
    Un formulaire pour créer ou mettre à jour un article dans la gestion de stock.
    """
    class Meta:
        model = Item
        fields = [
            'nom',
            'description',
            'categorie',
            'quantite',
            'prix',
            'date_expiration',
            'fournisseur'
        ]
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 2
                }
            ),
            'categorie': forms.Select(attrs={'class': 'form-control'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control'}),
            'prix': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'step': '0.01'
                }
            ),
            'date_expiration': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local'
                }
            ),
            'fournisseur': forms.Select(attrs={'class': 'form-control'}),
        }


class CategoryForm(forms.ModelForm):
    """
    Un formulaire pour créer ou mettre à jour une categorie dans la gestion de stock.
    """
    class Meta:
        model = Category
        fields = ['nom']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrer le nom de la catégorie',
                'aria-label': 'Nom de la catégorie',
            }),
        }
        labels = {
            'nom': 'Nom de la catégorie',
        }


class DeliveryForm(forms.ModelForm):
    """
    Un formulaire pour créer ou mettre à jour une livraison dans la gestion de stock.
    """
    class Meta:
        model = Delivery
        fields = [
            'article',
            'nom_client',
            'numero_telephone',
            'localisation',
            'date',
            'est_livré'
        ]
        widgets = {
            'article': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Selectionner un article',
            }),
            'nom_client': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrer le nom du client',
            }),
            'numero_telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrer le numéro de téléphone',
            }),
            'localisation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrer le lieu de livraison',
            }),
            'date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrer la date et l\'heure de livraison',
                'type': 'datetime-local'
            }),
            'est_livré': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'label': 'Marquer comme livré',
            }),
        }
