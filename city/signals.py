from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Patrol2, Share
from datetime import datetime
import logging

# Get an instance of a logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from background_task import background


# @background(schedule=1)
# def background_gen_small_points(
#     building_id, user_id, generated_people, generated_points
# ):
#     patrol = get_object_or_404(Patrol, id=user_id)
#     patrol.people += generated_people
#     patrol.points += generated_points
#     patrol.save()
#     print(
#         building_id,
#         "generated (pts, ppl)",
#         generated_people,
#         generated_points,
#         patrol.user.username,
#     )

INTERVAL = 60


@background(schedule=1)
def background_generate_resources(patrol_id):
    try:
        patrol = Patrol2.objects.get(id=patrol_id)
    except Patrol2.DoesNotExist as exc:
        logger.critical(patrol_id, exc)
        return

    shares = patrol.share_set.all()
    money_generated = 0
    people_generated = 0

    for share in shares:
        if share.building.is_built():
            # logger.info(share.building.name, share.building.generate_points)
            money_generated += (
                share.building.generate_points / share.building.max_shares
            )
            people_generated += (
                share.building.generate_people / share.building.max_shares
            )
        else:
            logger.info(f"{share.building.name} not built")

    logger.info(
        f"{shares.count()} shares generated {money_generated} money, {people_generated} ppl"
    )
    patrol.money += money_generated
    patrol.people += people_generated
    patrol.save()
    logger.info(f"{patrol} has now {patrol.money} money, {patrol.people} ppl")


@receiver(post_save, sender=Patrol2)
def create_task(sender, instance, created, **kwargs):
    if created:
        background_generate_resources(instance.id, repeat=INTERVAL)
        logger.info(f"created gen task for {instance.id}")


@receiver(post_save, sender=User)
def create_patrol(sender, instance, created, **kwargs):
    if created:
        Patrol2.objects.create(user=instance, name=f"Patrol {instance.username}")
        logger.info(f"created gen task for {instance.id}")


@receiver(post_save, sender=User)
def save_patrol(sender, instance, **kwargs):
    instance.patrol2.save()


@receiver(post_save, sender=Share)
def set_building_state(sender, instance: Share, created, **kwargs):
    b = instance.building
    if b.max_shares <= b.share_set.count():
        if b.datetime_build_started is None:
            b.datetime_build_started = datetime.now()
            logger.info(f"{b} build started")
    else:
        b.datetime_build_started = None
    b.save()
