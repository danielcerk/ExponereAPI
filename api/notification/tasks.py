from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.conf import settings

from celery import shared_task

User = get_user_model()

MAILGUN_WELCOME_EMAIL_TEMPLATE = settings.MAILGUN_WELCOME_EMAIL_TEMPLATE
MAILGUN_PASSWORD_RESET_EMAIL_TEMPLATE = settings.MAILGUN_PASSWORD_RESET_EMAIL_TEMPLATE
MAILGUN_CONFIRMATION_EMAIL_TEMPLATE = settings.MAILGUN_CONFIRMATION_EMAIL_TEMPLATE

@shared_task()
def send_welcome_email_task(email, username):

    message = EmailMessage(
        subject="Bem-vindo à Exponere",
        body="",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],
    )

    message.template_id = MAILGUN_WELCOME_EMAIL_TEMPLATE
    message.merge_global_data = {
        "name": username
    }

    try:

        message.send()

    except Exception as e:

        print("Erro ao enviar email:", e)

@shared_task()
def send_password_reset_email_task(user, reset_url):

    message = EmailMessage(
        subject="Redefinição de senha - Exponere",
        body="",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )

    message.template_id = MAILGUN_PASSWORD_RESET_EMAIL_TEMPLATE

    message.merge_global_data = {
        "name": user.username,
        "reset_url": reset_url,
        "reset_password_url": reset_url
    }

    try:

        message.send()

    except Exception as e:

        print("Erro ao enviar email:", e)

@shared_task()
def send_password_changed_email_task(user):

    message = EmailMessage(
        subject="Sua senha foi alterada - Exponere",
        body="",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )

    message.template_id = MAILGUN_CONFIRMATION_EMAIL_TEMPLATE

    message.merge_global_data = {
        "name": user.username
    }

    try:

        message.send()

    except Exception as e:

        print("Erro ao enviar email:", e)