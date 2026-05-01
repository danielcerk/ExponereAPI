from django.shortcuts import get_object_or_404
from django.db.models import Sum, F, DecimalField, ExpressionWrapper
from django.utils import timezone
from datetime import timedelta

from api.catalog.models import Catalog

from api.wishlist.models import Wishlist
from api.customer.models import Customer

def get_catalog(id):
    
    return get_object_or_404(Catalog, user__pk=id)

def apply_date_filter(qs, start_date=None, end_date=None, days=None):

    if days:

        start_date = timezone.now() - timedelta(days=days)

    if start_date:

        qs = qs.filter(created_at__gte=start_date)

    if end_date:

        qs = qs.filter(created_at__lte=end_date)

    return qs

def get_all_customer(id, start_date=None, end_date=None, days=None):

    cat = get_catalog(id)

    qs = Customer.objects.filter(

        catalog=cat

    )

    qs = apply_date_filter(qs, start_date, end_date, days)

    return qs.count()

def get_all_wishlist(id, start_date=None, end_date=None, days=None):

    cat = get_catalog(id)

    qs = Wishlist.objects.filter(
        product__catalog=cat,
    )

    qs = apply_date_filter(qs, start_date, end_date, days)

    return qs.values('session_key').distinct().count()