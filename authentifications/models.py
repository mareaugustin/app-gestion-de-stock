from django.db import models
from django.contrib.auth.models import User

from django_extensions.db.fields import AutoSlugField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from phonenumber_field.modelfields import PhoneNumberField


# Définir les statut et le rôle d'un profil
STATUS_CHOICES = [
    ('INA', 'Inactive'),
    ('ON', 'Active'),
    ('OL', 'On leave')
]

ROLE_CHOICES = [
    ('OP', 'Operative'),
    ('EX', 'Executive'),
    ('AD', 'Admin')
]


class Profile(models.Model):
    """
    Représente un profil utilisateur contenant des détails personnels et liés à l'authentification.
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='User'
    )
    slug = AutoSlugField(
        unique=True,
        verbose_name='Authentification ID',
        populate_from='email'
    )
    photo_profil = ProcessedImageField(
        default='profile_pics/avatar.jpg',
        upload_to='profile_pics',
        format='JPEG',
        processors=[ResizeToFill(150, 150)],
        options={'quality': 100}
    )
    telephone = PhoneNumberField(
        null=True, blank=True, verbose_name='Telephone'
    )
    email = models.EmailField(
        max_length=150, blank=True, null=True, verbose_name='Email'
    )
    prenom = models.CharField(
        max_length=30, blank=True, verbose_name='Prenom'
    )
    nom = models.CharField(
        max_length=30, blank=True, verbose_name='Nom'
    )
    statut = models.CharField(
        choices=STATUS_CHOICES,
        max_length=12,
        default='ON',
        verbose_name='Statut'
    )
    role = models.CharField(
        choices=ROLE_CHOICES,
        max_length=12,
        blank=True,
        null=True,
        verbose_name='Rôle'
    )

    @property
    def image_url(self):
        """
        Renvoie l'URL de la photo de profil.
        Renvoie une chaîne vide si l'image n'est pas disponible.
        """
        try:
            return self.photo_profil.url
        except AttributeError:
            return ''

    def __str__(self):
        """
        Renvoie une représentation sous forme de chaîne du profil.
        """
        return f"{self.user.username} Profile"

    class Meta:
        """Options Meta pour le modèle Profile"""
        ordering = ['slug']
        verbose_name = 'Profil'
        verbose_name_plural = 'Profils'


class Vendor(models.Model):
    """
    Représente un fournisseur avec des informations de contact et d'adresse.
    """
    nom = models.CharField(max_length=50, verbose_name='Nom', default="Inconnu")
    slug = AutoSlugField(
        unique=True,
        populate_from='nom',
        verbose_name='Slug'
    )
    numero_phone = models.BigIntegerField(
        blank=True, null=True, verbose_name='Numero de téléphone'
    )
    addresse = models.CharField(
        max_length=50, blank=True, null=True, verbose_name='Addresse'
    )

    def __str__(self):
        """
        Renvoie une représentation sous forme de chaîne du fournisseur.
        """
        return self.nom

    class Meta:
        """Options Meta pour le model fournisseur."""
        verbose_name = 'Fournisseur'
        verbose_name_plural = 'Fournisseurs'


class Customer(models.Model):
    prenom = models.CharField(max_length=256)
    nom = models.CharField(max_length=256, blank=True, null=True)
    addresse = models.TextField(max_length=256, blank=True, null=True)
    email = models.EmailField(max_length=256, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    point_fidelite = models.IntegerField(default=0)

    class Meta:
        db_table = 'Customers'

    def __str__(self) -> str:
        return self.prenom + " " + self.nom

    def get_full_name(self):
        return self.prenom + " " + self.nom

    def to_select2(self):
        item = {
            "label": self.get_full_name(),
            "value": self.id
        }
        return item
