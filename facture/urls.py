# Django core imports
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# Importations des applications locales
from .views import (
    FactureListView,
    FactureDetailView,
    FactureCreateView,
    FactureUpdateView,
    FactureDeleteView
)

# URL patterns
urlpatterns = [
    # URLs factures
    path(
        'factures/',
        FactureListView.as_view(),
        name='facturelist'
    ),
    path(
        'facture/<slug:slug>/',
        FactureDetailView.as_view(),
        name='facture-detail'
    ),
    path(
        'new-facture/',
        FactureCreateView.as_view(),
        name='facture-create'
    ),
    path(
        'facture/<slug:slug>/update/',
        FactureUpdateView.as_view(),
        name='facture-update'
    ),
    path(
        'facture/<int:pk>/delete/',
        FactureDeleteView.as_view(),
        name='facture-delete'
    ),
]

# Configuration des fichiers médias statiques pour le développement.
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
