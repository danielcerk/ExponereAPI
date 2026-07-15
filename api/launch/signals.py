from django.db.models.signals import post_save
from django.dispatch import receiver

from api.launch.models import Launch
from api.launch.tasks import send_marketing_launch


@receiver(post_save, sender=Launch)
def send_confirm_email_launch(sender, instance, created, **kwargs):

    if not created:

        return

    send_marketing_launch.delay(instance.id)