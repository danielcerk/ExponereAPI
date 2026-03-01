from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import UserProfile, Profile

@receiver(post_save, sender=UserProfile)
def create_profile_user(sender, instance, created, **kwargs):
    
    if created and not Profile.objects.filter(user=instance).exists():

        Profile.objects.create(
            user=instance,
        )
		