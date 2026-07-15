from django.core.mail import EmailMessage
from django.conf import settings

from celery import shared_task

'''@shared_task()
def send_marketing_launch(order_id):

    message_to_customer = EmailMessage(
        subject=f"Confirmação de pedido #{order.id} - {order.catalog.name}",
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[order.customer.email],
    )'''