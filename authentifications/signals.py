from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def handle_user_profile(sender, instance, created, **kwargs):
    """
    Gestionnaire de signal pour créer ou mettre à jour un profil lorsqu'un utilisateur est enregistré.
    """
    if created:
        Profile.objects.create(user=instance)
        print('Profil créé!')
    else:
        instance.profile.save()
        print('Profil mis à jour!')
