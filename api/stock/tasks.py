from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.conf import settings

from celery import shared_task

User = get_user_model()

MAILGUN_REMINDER_PRODUCT_EMAIL_TEMPLATE = settings.MAILGUN_REMINDER_PRODUCT_EMAIL_TEMPLATE

@shared_task()
def send_reminder_product_stock_available(email, store, product):


    message = EmailMessage(
        subject=f"{product.name} está disponível novamente!",
        body="",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],
    )

    message.template_id = MAILGUN_REMINDER_PRODUCT_EMAIL_TEMPLATE

    message.merge_global_data = {
        "email": email,
        "product_name": product.name,
        "product_price": f"{product.price:.2f}".replace(".", ","),
        "product_url": f"{settings.SITE_URL}/produto/{product.id}/",
        "store_name": getattr(store, "name", "Loja"),
    }

    try:

        message.send()

    except Exception as e:

        print("Erro ao enviar email:", e)