from django.db.models.signals import post_save
from django.dispatch import receiver

from api.marketing_launch.models import MarketingLaunch
from api.marketing_launch.tasks import send_marketing_launch_campaign


@receiver(post_save, sender=MarketingLaunch)
def send_email_marketing_camapign_launch(sender, instance, created, **kwargs):

    if not created:

        return

    send_marketing_launch_campaign.delay(instance.id)