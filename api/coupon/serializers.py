from rest_framework import serializers

from .models import (
    CouponProgressive,
    CouponFixedValue,
    CouponPercentValue,
    CouponFirstBuy,
    CouponUsage
)

class BaseCouponSerializer(serializers.ModelSerializer):

    is_valid_coupon = serializers.SerializerMethodField(read_only=True)

    class Meta:
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
            "is_valid_coupon",
            "min_purchase_value"
        ]
        read_only_fields = (
            "id",
            "catalog",
            "usage_count", 
            "created_at", 
            "updated_at"
        )

        extra_kwargs = {

            "is_active": {"required": False},
            "is_valid_coupon": {"required": False}

        }

    def get_is_valid_coupon(self, obj):

        return obj.is_valid()

    def validate(self, data):

        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if start_date and end_date and start_date > end_date:
            
            raise serializers.ValidationError(
                "A data de início não pode ser maior que a data de expiração."
            )

        return data

class CouponProgressiveSerializer(BaseCouponSerializer):

    class Meta(BaseCouponSerializer.Meta):

        model = CouponProgressive
        fields = BaseCouponSerializer.Meta.fields + [
            "min_purchase_value",
            "max_purchase_value",
            "percent_discount",
        ]

    def validate(self, data):
        
        data = super().validate(data)

        min_val = data.get("min_purchase_value")
        max_val = data.get("max_purchase_value")

        if min_val and max_val and min_val > max_val:
            raise serializers.ValidationError(
                "O valor mínimo não pode ser maior que o valor máximo."
            )

        return data

class CouponFixedValueSerializer(BaseCouponSerializer):

    class Meta(BaseCouponSerializer.Meta):

        model = CouponFixedValue
        fields = BaseCouponSerializer.Meta.fields + [
            "discount_value",
            "min_purchase_value",
        ]

class CouponPercentValueSerializer(BaseCouponSerializer):

    class Meta(BaseCouponSerializer.Meta):
        model = CouponPercentValue
        fields = BaseCouponSerializer.Meta.fields + [
            "percent_discount",
            "min_purchase_value",
            "max_discount_value",
        ]

    def validate(self, data):

        data = super().validate(data)

        percent = data.get("percent_discount")

        if percent and percent > 100:

            raise serializers.ValidationError(
                "O percentual não pode ser maior que 100%."
            )

        return data

class CouponFirstBuySerializer(BaseCouponSerializer):

    class Meta(BaseCouponSerializer.Meta):

        model = CouponFirstBuy
        fields = BaseCouponSerializer.Meta.fields + [
            "percent_discount",
            "min_purchase_value",
        ]

class CouponUsageSerializer(serializers.ModelSerializer):

    class Meta:

        model = CouponUsage
        fields = '__all__'

        read_only_fields = ("coupon", "customer", "order", "created_at", "updated_at")

class CouponDynamicSerializer(serializers.Serializer):

    def to_representation(self, instance):

        if hasattr(instance, "couponprogressive"):

            return CouponProgressiveSerializer(instance.couponprogressive).data

        if hasattr(instance, "couponfixedvalue"):

            return CouponFixedValueSerializer(instance.couponfixedvalue).data

        if hasattr(instance, "couponpercentvalue"):

            return CouponPercentValueSerializer(instance.couponpercentvalue).data

        if hasattr(instance, "couponfirstbuy"):
            
            return CouponFirstBuySerializer(instance.couponfirstbuy).data

        return None