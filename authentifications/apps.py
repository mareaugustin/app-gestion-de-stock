from django.apps import AppConfig


class AuthentificationsConfig(AppConfig):
    """La configuration pour l'application authentifications."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentifications'

    def ready(self):
        """Import signals pour l'application authentifications."""
        import authentifications.signals
