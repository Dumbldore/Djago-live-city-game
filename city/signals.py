from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Patrol2
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


@receiver(post_save, sender=Patrol2)
def create_task(sender, instance, created, **kwargs):
    if created:
        pass


@receiver(post_save, sender=User)
def create_patrol(sender, instance, created, **kwargs):
    if created:
        Patrol2.objects.create(user=instance)
