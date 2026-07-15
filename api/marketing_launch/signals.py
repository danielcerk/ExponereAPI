from django.dispatch import receiver
from django.db.models.signals import post_save

from api.auth.models import UserProfile

from .models import MarketingLaunch


'''@receiver(post_save, sender=UserProfile)
def send_confirm_email_launch(sender, instance, created, **kwargs):
    
    if created and not Launch.objects.filter(email=instance.email).exists():
'''