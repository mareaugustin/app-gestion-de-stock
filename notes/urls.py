# Django core imports
from django.urls import path

# Importations des apllications locales
from .views import (
    NoteListView,
    NoteCreateView,
    NoteUpdateView,
    NoteDeleteView
)

# URL patterns
urlpatterns = [
    # URLs pour les notes
    path(
        'notes/',
        NoteListView.as_view(),
        name='note_list'
    ),
    path('new-note/', NoteCreateView.as_view(), name='note_create'),
    path(
        'note/<slug:slug>/update/',
        NoteUpdateView.as_view(),
        name='note_update'
    ),
    path(
        'note/<int:pk>/delete/',
        NoteDeleteView.as_view(),
        name='note_delete'
    ),
]
