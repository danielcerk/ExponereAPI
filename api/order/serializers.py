from django.shortcuts import get_object_or_404

from rest_framework import serializers

from .models import Order, ProductOrder

from api.nf.serializers import NFSerializer
from api.wishlist.serializers import WishlistSerializer
from api.customer.serializers import CustomerSerializer
from api.catalog.serializers import CatalogSerializer
from api.coupon.serializers import CouponDynamicSerializer
from api.nf.models import NF
from api.customer.models import Customer
from api.catalog.models import Catalog
from api.wishlist.models import Wishlist
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

    customer = CustomerSerializer(required=True)
    catalog = CatalogSerializer(read_only=True)

    coupon = CouponDynamicSerializer(read_only=True)

    coupon_code = serializers.CharField(
        write_only=True,
        required=False,
        allow_null=True,
        allow_blank=True
    )

    nf = serializers.SerializerMethodField()
    nf_data = NFSerializer(write_only=True, required=False)

    items = ProductOrderSerializer(many=True)

    class Meta:
        
        model = Order
        fields = [
            'id',
            'catalog',
            'customer',
            'subtotal',
            'discount',
            'total',
            'coupon',
            'coupon_code',
            'is_paid',
            'payment_method',
            'items',
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

    def get_nf(self, obj):

        nf = NF.objects.filter(order=obj).first()

        return NFSerializer(nf).data if nf else None

    def create(self, validated_data):

        view = self.context["view"]

        catalog = get_object_or_404(
            Catalog,
            pk=view.kwargs["catalog_pk"]
        )

        items_data = validated_data.pop("items", [])
        nf_data = validated_data.pop("nf_data", None)
        coupon_code = validated_data.pop("coupon_code", None)
        customer_data = validated_data.pop("customer", None)

        customer = Customer.objects.filter(
            catalog=catalog,
            email=customer_data["email"]
        ).first()

        if customer:

            customer_serializer = CustomerSerializer(

                customer,
                data=customer_data,
                context={"request": self.context.get("request")},
                partial=True

            )

        else:
            
            customer_serializer = CustomerSerializer(
                data=customer_data,
                context={"request": self.context.get("request")},
            )

        customer_serializer.is_valid(raise_exception=True)
        customer = customer_serializer.save(catalog=catalog)

        order = Order.objects.create(
            catalog=catalog,
            customer=customer,
            **validated_data
        )

        wishlist_ids = []

        for item in items_data:

            wishlist_product = item["wishlist_product"]

            get_wishlist = get_object_or_404(Wishlist, pk=wishlist_product.id, is_active=True)

            if get_wishlist:

                ProductOrder.objects.create(
                    order=order,
                    wishlist_product=wishlist_product
                )

                wishlist_ids.append(wishlist_product.id)

        if wishlist_ids:

            Wishlist.objects.filter(id__in=wishlist_ids).update(is_active=False)

        if coupon_code:

            coupon = get_coupon_by_code(catalog, coupon_code)

            if not coupon:

                raise serializers.ValidationError({
                    "coupon_code": "Cupom inválido, expirado ou indisponível."
                })

            if not coupon.is_valid():

                raise serializers.ValidationError({
                    "coupon_code": "Cupom não pode ser utilizado."
                })

            order.coupon = coupon

        if nf_data:

            request = self.context.get("request")
            file = request.FILES.get("nf_data.file")

            if file:

                nf_data["file"] = file

            nf_serializer = NFSerializer(data=nf_data)
            nf_serializer.is_valid(raise_exception=True)
            nf_serializer.save(order=order)

        order.calculate_totals()
        order.save()

        return order

    def update(self, instance, validated_data):

        items_data = validated_data.pop('items', None)
        nf_data = validated_data.pop('nf_data', None)
        customer_data = validated_data.pop('customer', None)
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

            request = self.context.get("request")
            file = request.FILES.get("nf_data.file")

            if file:

                nf_data["file"] = file

            nf = NF.objects.filter(order=instance).first()

            if nf:

                nf_serializer = NFSerializer(
                    nf,
                    data=nf_data,
                    partial=True
                )

            else:

                nf_serializer = NFSerializer(data=nf_data)

            nf_serializer.is_valid(raise_exception=True)
            nf_serializer.save(order=instance)

        if customer_data is not None:

            customer = instance.customer

            if customer:

                for attr, value in customer_data.items():

                    setattr(customer, attr, value)

                customer.save()

        instance.calculate_totals()
        instance.save()

        return instance