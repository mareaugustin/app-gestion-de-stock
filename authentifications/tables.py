import django_tables2 as tables
from django.shortcuts import render

from .models import Profile


class ProfileTable(tables.Table):
    """Représentation sous forme de table pour le modèle Profile."""

    class Meta:
        """Options Meta pour le ProfileTable."""
        model = Profile
        template_name = "django_tables2/semantic.html"
        fields = (
            'date',
            'nom_client',
            'numero_telephone',
            'article',
            'prix_par_article',
            'quantite',
            'total'
        )
        order_by_field = 'sort'
