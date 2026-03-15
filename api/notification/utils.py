from django.core.mail import EmailMessage
from django.conf import settings

import os

def send_password_reset_email(user, reset_url):

    message = EmailMessage(
        subject="Redefinição de senha - Exponere",
        body="",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )

    message.template_id = os.environ['MAILGUN_PASSWORD_RESET_EMAIL_TEMPLATE']

    message.merge_data = {
        user.email: {
            "name": user.first_name,
            "reset_url": reset_url
        }
    }

    message.send()

def send_password_changed_email(user):

    message = EmailMessage(
        subject="Sua senha foi alterada - Exponere",
        body="",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )

    message.template_id = os.environ['MAILGUN_CONFIRMATION_EMAIL_TEMPLATE']

    message.merge_data = {
        user.email: {
            "name": user.first_name
        }
    }

    message.send()