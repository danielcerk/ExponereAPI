from django.core.mail import EmailMessage
from django.conf import settings

from celery import shared_task

from .models import Order, ProductOrder


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