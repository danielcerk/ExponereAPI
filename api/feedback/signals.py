from django.db.models.signals import post_save
from django.dispatch import receiver

from api.feedback.models import Feedback
from api.feedback.tasks import send_marketing_feedback


@receiver(post_save, sender=Feedback)
def send_confirm_email_feedback(sender, instance, created, **kwargs):

    if not created:

        return

    send_marketing_feedback.delay(instance.id)