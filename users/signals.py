from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Patrol


@receiver(post_save, sender=User)
def create_patrol(sender, instance, created, **kwargs):
    if created:
        Patrol.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_patrol(sender, instance, **kwargs):
    instance.patrol.save()
