from django.contrib import admin
from .models import Profile, Vendor


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Interface administrateur pour le model profil."""
    list_display = ('user', 'telephone', 'email', 'role', 'statut')


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    """Interface administrateur pour le model fournisseur."""
    fields = ('nom', 'numero_phone', 'addresse')
    list_display = ('nom', 'numero_phone', 'addresse')
    search_fields = ('nom', 'numero_phone', 'addresse')
