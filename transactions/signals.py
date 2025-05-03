from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Purchase


@receiver(post_save, sender=Purchase)
def update_item_quantity(sender, instance, created, **kwargs):
    """
    Signal pour mettre à jour la quantité d'un article lorsqu'un achat est effectué.
    """
    if created:
        instance.article.quantite += instance.quantite
        instance.article.save()
