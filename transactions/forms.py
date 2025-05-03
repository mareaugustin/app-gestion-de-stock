from django import forms
from .models import Purchase


class BootstrapMixin(forms.ModelForm):
    """
    Un mixin pour ajouter des classes Bootstrap aux champs de formulaire.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')


class PurchaseForm(BootstrapMixin, forms.ModelForm):
    """
    Un formulaire pour créer et mettre à jour des instances de Purchase.
    """
    class Meta:
        model = Purchase
        fields = [
            'article',  'prix', 'description', 'fournisseur',
            'quantite', 'date_livraison', 'statut_livraison'
        ]
        widgets = {
            'date_livraison': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local'
                }
            ),
            'description': forms.Textarea(
                attrs={'rows': 1, 'cols': 40}
            ),
            'quantite': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),
            'statut_livraison': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'prix': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),
        }
