from rest_framework import serializers

from .models import *

from django.db import transaction

class CouponDynamicSerializer(serializers.ModelSerializer):

    min_purchase_value = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        allow_null=True,
    )

    percent_discount = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False,
        allow_null=True,
    )

    max_purchase_value = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        allow_null=True,
    )

    max_discount_value = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        allow_null=True,
    )

    discount_type = serializers.SerializerMethodField()
    discount_value = serializers.SerializerMethodField()
    is_valid_coupon = serializers.SerializerMethodField()

    class Meta:
        model = Coupon
        fields = [
            "id",
            "name",
            "code",
            "is_active",
            "usage_limit",
            "usage_count",
            "start_date",
            "end_date",
            "created_at",
            "updated_at",
            "discount_type",
            "discount_value",
            "is_valid_coupon",
            "min_purchase_value",
            "percent_discount",
            "max_purchase_value",
            "max_discount_value",
        ]

    def get_discount_type(self, obj):

        coupon = obj.get_real_instance()

        return coupon.discount_type

    def get_discount_value(self, obj):

        if hasattr(obj, "couponprogressive"):
            return obj.couponprogressive.percent_discount

        if hasattr(obj, "couponfixedvalue"):
            return obj.couponfixedvalue.discount_value

        if hasattr(obj, "couponpercentvalue"):
            return obj.couponpercentvalue.percent_discount

        if hasattr(obj, "couponfirstbuy"):
            return obj.couponfirstbuy.percent_discount

        return None

    def get_is_valid_coupon(self, obj):

        return obj.is_valid()

    def to_representation(self, instance):

        coupon = instance.get_real_instance()

        data = {
            "id": coupon.id,
            "name": coupon.name,
            "code": coupon.code,
            "is_active": coupon.is_active,
            "usage_limit": coupon.usage_limit,
            "usage_count": coupon.usage_count,
            "start_date": coupon.start_date,
            "end_date": coupon.end_date,
            "created_at": coupon.created_at,
            "updated_at": coupon.updated_at,
            "discount_type": coupon.discount_type,
            "is_valid_coupon": coupon.is_valid(),

            "discount_value": None,
            "percent_discount": None,
            "min_purchase_value": None,
            "max_purchase_value": None,
            "max_discount_value": None,
        }

        if isinstance(coupon, CouponFixedValue):
            data["discount_value"] = coupon.discount_value
            data["min_purchase_value"] = coupon.min_purchase_value

        elif isinstance(coupon, CouponPercentValue):
            data["percent_discount"] = coupon.percent_discount
            data["min_purchase_value"] = coupon.min_purchase_value
            data["max_discount_value"] = coupon.max_discount_value

        elif isinstance(coupon, CouponProgressive):
            data["percent_discount"] = coupon.percent_discount
            data["min_purchase_value"] = coupon.min_purchase_value
            data["max_purchase_value"] = coupon.max_purchase_value

        elif isinstance(coupon, CouponFirstBuy):
            data["percent_discount"] = coupon.percent_discount
            data["min_purchase_value"] = coupon.min_purchase_value

        return data

    def change_coupon_type(
        self,
        coupon,
        discount_type,
        data,
    ):

        parent = Coupon.objects.get(pk=coupon.pk)

        if hasattr(parent, "couponprogressive"):
            parent.couponprogressive.delete()

        if hasattr(parent, "couponfixedvalue"):
            parent.couponfixedvalue.delete()

        if hasattr(parent, "couponpercentvalue"):
            parent.couponpercentvalue.delete()

        if hasattr(parent, "couponfirstbuy"):
            parent.couponfirstbuy.delete()

        mapping = {
            "fixed": CouponFixedValue,
            "percentage": CouponPercentValue,
            "progressive": CouponProgressive,
            "first_buy": CouponFirstBuy,
        }

        model = mapping[discount_type]

        fields = {}

        if discount_type == "fixed":
            fields["discount_value"] = data.get("discount_value")
            fields["min_purchase_value"] = data.get("min_purchase_value")

        elif discount_type == "percentage":
            fields["percent_discount"] = data.get("percent_discount")
            fields["min_purchase_value"] = data.get("min_purchase_value")
            fields["max_discount_value"] = data.get("max_discount_value")

        elif discount_type == "progressive":
            fields["percent_discount"] = data.get("percent_discount")
            fields["min_purchase_value"] = data.get("min_purchase_value")
            fields["max_purchase_value"] = data.get("max_purchase_value")

        elif discount_type == "first_buy":
            fields["percent_discount"] = data.get("percent_discount")
            fields["min_purchase_value"] = data.get("min_purchase_value")

        new_coupon = model.objects.create(
            coupon_ptr=parent,
            **fields,
        )

        return new_coupon

    def update(self, instance, validated_data):

        with transaction.atomic():

            coupon = instance.get_real_instance()

            new_type = validated_data.pop(
                "discount_type",
                coupon.discount_type,
            )

            common_fields = [
                "name",
                "code",
                "is_active",
                "usage_limit",
                "start_date",
                "end_date",
            ]

            common_data = {}

            for field in common_fields:

                if field in validated_data:
                    value = validated_data.pop(field)
                    setattr(coupon, field, value)
                    common_data[field] = value

            coupon.save()

            if new_type != coupon.discount_type:

                return self.change_coupon_type(
                    coupon,
                    new_type,
                    validated_data,
                )

            for field, value in validated_data.items():

                if hasattr(coupon, field):
                    setattr(coupon, field, value)

            coupon.save()

            return coupon