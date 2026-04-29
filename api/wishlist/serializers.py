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
        
        extra_kwargs = {

            'id': {'required': False},

        }

    def validate_quantity(self, value):

        if value <= 0:

            raise serializers.ValidationError(

                "Quantity must be greater than zero."

            )

        return value

    def validate(self, attrs):
        request = self.context.get('request')

        session = request.session

        if not session.session_key:
            session.save()

        attrs['session_key'] = session.session_key

        return attrs