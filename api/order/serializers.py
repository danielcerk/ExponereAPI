from rest_framework import serializers

from api.nf.serializers import NFSerializer

from api.wishlist.serializers import WishlistSerializer
from api.customer.serializers import CustomerSerializer
from api.catalog.serializers import CatalogSerializer
from api.coupon.serializers import CouponDynamicSerializer

from .models import Order, ProductOrder
from api.nf.models import NF

from api.coupon.utils import get_coupon_by_code

class ProductOrderSerializer(serializers.ModelSerializer):

    wishlist_product = WishlistSerializer(read_only=True)
    wishlist_product_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductOrder._meta.get_field('wishlist_product').related_model.objects.all(),
        source='wishlist_product',
        write_only=True
    )

    class Meta:
        model = ProductOrder
        fields = [
            'id',
            'wishlist_product',
            'wishlist_product_id',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class OrderSerializer(serializers.ModelSerializer):

    customer = CustomerSerializer(read_only=True)
    catalog = CatalogSerializer(read_only=True)
    coupon = CouponDynamicSerializer(read_only=True)

    coupon_code = serializers.CharField(write_only=True, required=False)

    nf = serializers.SerializerMethodField()
    nf_data = NFSerializer(write_only=True, required=False)

    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Order._meta.get_field('customer').related_model.objects.all(),
        source='customer',
        write_only=True
    )

    catalog_id = serializers.PrimaryKeyRelatedField(
        queryset=Order._meta.get_field('catalog').related_model.objects.all(),
        source='catalog',
        write_only=True
    )

    items = ProductOrderSerializer(many=True)
    total_items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id',
            'catalog',
            'catalog_id',
            'customer',
            'customer_id',
            'subtotal',
            'discount',
            'total',
            'coupon',
            'is_paid',
            'payment_method',
            'items',
            'total_items',
            'nf', 
            'nf_data',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'subtotal',
            'discount',
            'total',
            'created_at',
            'updated_at'
        ]

    def get_total_items(self, obj):

        return obj.items.count()

    def get_nf(self, obj):

        nf = NF.objects.filter(order=obj).first()

        return NFSerializer(nf).data if nf else None

    def create(self, validated_data):

        items_data = validated_data.pop('items', [])
        nf_data = validated_data.pop('nf_data', None)
        coupon_code = validated_data.pop('coupon_code', None)

        order = Order.objects.create(**validated_data)

        for item in items_data:

            ProductOrder.objects.create(
                order=order,
                wishlist_product=item['wishlist_product']
            )

        if coupon_code:

            coupon = get_coupon_by_code(order.catalog, coupon_code)

            if coupon and coupon.is_valid():

                order.coupon = coupon

        if nf_data:

            NF.objects.create(order=order, **nf_data)

        order.calculate_totals()
        order.save()

        return order

    def update(self, instance, validated_data):

        items_data = validated_data.pop('items', None)
        nf_data = validated_data.pop('nf_data', None)
        coupon_code = validated_data.pop('coupon_code', None)

        for attr, value in validated_data.items():
            
            setattr(instance, attr, value)

        if items_data is not None:

            instance.items.all().delete()

            for item in items_data:
                ProductOrder.objects.create(
                    order=instance,
                    wishlist_product=item['wishlist_product']
                )

        if coupon_code:

            coupon = get_coupon_by_code(instance.catalog, coupon_code)

            if coupon and coupon.is_valid():

                instance.coupon = coupon

        if nf_data is not None:

            nf = NF.objects.filter(order=instance).first()

            if nf:

                for attr, value in nf_data.items():

                    setattr(nf, attr, value)

                nf.save()

            else:

                NF.objects.create(order=instance, **nf_data)

        instance.calculate_totals()
        instance.save()

        return instance