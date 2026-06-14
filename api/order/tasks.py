from django.core.mail import EmailMessage
from django.conf import settings

from celery import shared_task

from .models import Order, ProductOrder
from api.notification.models import Notification

@shared_task()
def create_notification_order_customer(order_id):

    order = Order.objects.select_related(
        "catalog",
        "customer",
        "catalog__user"
    ).prefetch_related(
        "items__wishlist_product__product"
    ).get(id=order_id)

    Notification.objects.create(
        catalog=order.catalog,
        user=order.catalog.user,
        type_notification=Notification.NotificationType.ORDER,
        title=f"Novo pedido #{order.id}",
        message=(
            f"{order.customer.full_name} realizou um pedido "
            f"no valor de R$ {order.total}."
        ),
        action_url=f"/admin/orders/{order.id}",
        payload={
            "order_id": order.id,
            "customer_name": order.customer.full_name,
            "customer_email": order.customer.email,
            "total": str(order.total),
            "is_paid": order.is_paid,
            "payment_method": order.payment_method,
        }
    )

@shared_task()
def send_confirmation_order_customer(order_id):

    order = Order.objects.select_related(
        "catalog",
        "customer"
    ).prefetch_related(
        "items__wishlist_product__product"
    ).get(id=order_id)

    items_text = ""

    for item in order.items.all():
        
        wishlist = item.wishlist_product

        items_text += (
            f"- {wishlist.product.title} | "
            f"Qtd: {wishlist.quantity} | "
            f"Preço: R$ {wishlist.product.price}\n"
        )

    body = f"""
Pedido #{order.id}
Catálogo: {order.catalog.name}

========================
DADOS DO CLIENTE
========================
Nome: {order.customer.full_name}
Email: {order.customer.email}

========================
ITENS DO PEDIDO
========================
{items_text}

========================
RESUMO
========================
Subtotal: R$ {order.subtotal}
Desconto: R$ {order.discount}
Total: R$ {order.total}

Forma de pagamento: {order.payment_method or "Não informado"}
Status: {"Pago" if order.is_paid else "Pendente"}

Data do pedido: {order.created_at.strftime("%d/%m/%Y %H:%M")}
"""

    message_to_customer = EmailMessage(
        subject=f"Confirmação de pedido #{order.id} - {order.catalog.name}",
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[order.customer.email],
    )

    message_to_catalog_owner = EmailMessage(
        subject=f"Novo pedido #{order.id} - {order.catalog.name}",
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[order.catalog.user.email],
    )

    message_to_customer.send()
    message_to_catalog_owner.send()