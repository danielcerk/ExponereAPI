from rest_framework import serializers

from .models import Wishlist


class WishlistSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(
        source="product.name",
        read_only=True
    )

    class Meta:

        model = Wishlist

        fields = (
            "id",
            "product",
            "product_name",
            "quantity",
            "session_key",
            "is_active",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "session_key",
            "created_at",
            "updated_at",
        )

        extra_kwargs = {

            'id': {'required': False},
            'is_active': {'required': False}

        }

    def validate_quantity(self, value):

        if value <= 0:

            raise serializers.ValidationError(

                "Quantity must be greater than zero."

            )

        return value

    def validate(self, attrs):

        user = attrs.get("user")
        session_key = attrs.get("session_key")

        if not user and not session_key:

            raise serializers.ValidationError(

                "User or session_key must be provided."

            )

        return attrs