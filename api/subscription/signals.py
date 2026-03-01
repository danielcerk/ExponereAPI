from django.dispatch import receiver
from django.db.models.signals import post_save

from api.auth.models import UserProfile

from .models import CheckoutSessionRecord, Plan

@receiver(post_save, sender=UserProfile)
def create_checkout_session_user(sender, instance, created, **kwargs):
    
    if created and not CheckoutSessionRecord.objects.filter(user=instance).exists():

        get_first_plan, _ = Plan.objects.get_or_create(
            id=1, name='Free', price=0
        )

        CheckoutSessionRecord.objects.create(
            user=instance, plan=get_first_plan
        )
		