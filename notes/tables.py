import django_tables2 as tables
from .models import Note


class NoteTable(tables.Table):
    """Vue de tableau pour les notes."""

    class Meta:
        """Options Meta pour la table note."""
        model = Note
        template_name = "django_tables2/semantic.html"
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
        order_by_field = 'sort'
