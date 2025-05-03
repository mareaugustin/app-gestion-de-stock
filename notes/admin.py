from django.contrib import admin
from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """Interface d'administration pour gérer les instances de Note"""

    fields = (
        'date',
        'entreprise_nom',
        'numero_telephone',
        'email',
        'addresse',
        'description',
        'paiement_details',
        'montant',
        'statut'
    )

    list_display = (
        'slug',
        'date',
        'entreprise_nom',
        'numero_telephone',
        'email',
        'addresse',
        'description',
        'paiement_details',
        'montant',
        'statut'
    )
