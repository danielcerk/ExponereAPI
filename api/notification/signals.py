from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.conf import settings

User = get_user_model()

MAILGUN_WELCOME_EMAIL_TEMPLATE = settings.MAILGUN_WELCOME_EMAIL_TEMPLATE

'''@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):

    if not created:
        return

    message = EmailMessage(
        subject="Bem-vindo à Exponere",
        body="",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[instance.email],
    )

    message.template_id = MAILGUN_WELCOME_EMAIL_TEMPLATE
    message.merge_global_data = {
        "name": instance.username
    }

    try:
        message.send()
    except Exception as e:
        print("Erro ao enviar email:", e)'''