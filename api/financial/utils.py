from django.shortcuts import get_object_or_404
from django.db.models import Sum, F, DecimalField, ExpressionWrapper
from django.utils import timezone
from datetime import timedelta

from api.catalog.models import Catalog
from api.stock.models import StockMovement
from api.order.models import Order
from api.order.models import OrderItem


def get_catalog(id):
    
    return get_object_or_404(Catalog, pk=id)


def apply_date_filter(qs, start_date=None, end_date=None, days=None):

    if days:

        start_date = timezone.now() - timedelta(days=days)

    if start_date:

        qs = qs.filter(created_at__gte=start_date)

    if end_date:

        qs = qs.filter(created_at__lte=end_date)

    return qs


def revenue_catalog(id, start_date=None, end_date=None, days=None):

    cat = get_catalog(id)

    qs = Order.objects.filter(
        catalog=cat,
        is_paid=True,
    )

    qs = apply_date_filter(qs, start_date, end_date, days)

    return qs.aggregate(total=Sum('total'))['total'] or 0


def cost_catalog(id, start_date=None, end_date=None, days=None):

    cat = get_catalog(id)

    qs = StockMovement.objects.filter(
        stock__product__catalog=cat,
        type=StockMovement.IN
    )

    qs = apply_date_filter(qs, start_date, end_date, days)

    return qs.aggregate(
        total=Sum(
            ExpressionWrapper(
                F('purchase_price') * F('quantity'),
                output_field=DecimalField(max_digits=12, decimal_places=2)
            )
        )
    )['total'] or 0


def profit_catalog(id, **filters):

    return revenue_catalog(id, **filters) - cost_catalog(id, **filters)


def best_selling_product(id, **filters):

    cat = get_catalog(id)

    qs = OrderItem.objects.filter(
        order__catalog=cat,
        order__is_paid=True
    )

    qs = apply_date_filter(qs, filters.get('start_date'), filters.get('end_date'), filters.get('days'))

    return qs.values(
        'wishlist_product__product__id',
        'wishlist_product__product__name'
    ).annotate(

        total_sold=Sum('wishlist_product__quantity')

    ).order_by('-total_sold').first()


def worst_selling_product(id, **filters):

    cat = get_catalog(id)

    qs = OrderItem.objects.filter(
        order__catalog=cat,
        order__is_paid=True
    )

    qs = apply_date_filter(qs, filters.get('start_date'), filters.get('end_date'), filters.get('days'))

    return qs.values(
        'wishlist_product__product__id',
        'wishlist_product__product__name'
    ).annotate(

        total_sold=Sum('wishlist_product__quantity')

    ).order_by('total_sold').first()