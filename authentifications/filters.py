import django_filters
from .models import Profile


class StaffFilter(django_filters.FilterSet):
    """."""

    class Meta:
        """Meta options pour la class."""
        model = Profile
        fields = ['user', 'email', 'role', 'statut']
