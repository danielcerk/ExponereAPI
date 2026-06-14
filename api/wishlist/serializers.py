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
            "is_active",
            "created_at",
            "updated_at",
        )

    def validate_quantity(self, value):

        if value <= 0:

            raise serializers.ValidationError(
                "Quantity must be greater than zero."
            )
        
        return value

    def validate(self, attrs):

        request = self.context.get("request")
        session = request.session

        if not session.session_key:

            session.save()

        attrs["session_key"] = session.session_key

        return attrs

    def create(self, validated_data):

        product = validated_data["product"]
        session_key = validated_data["session_key"]
        quantity = validated_data.get("quantity", 1)

        wishlist = Wishlist.objects.filter(
            product=product,
            session_key=session_key,
            is_active=True
        ).first()

        if wishlist:

            wishlist.quantity += quantity
            wishlist.save(update_fields=["quantity", "updated_at"])

            return wishlist

        return Wishlist.objects.create(**validated_data)