from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import UserProfile, Profile

from api.address.models import Address

from api.notification.tasks import send_welcome_email_task

@receiver(post_save, sender=UserProfile)
def create_profile_user(sender, instance, created, **kwargs):
    
    if created and not Profile.objects.filter(user=instance).exists():
        
        address = Address.objects.create()
        Profile.objects.create(
            user=instance, address=address
        )

        # send_welcome_email_task.delay(

        #     instance.email, instance.username

        # )
		