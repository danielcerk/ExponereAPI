from rest_framework import serializers
from .models import Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"

        extra_kwargs = {
            "id": {"required": False},
            "street": {"required": False},
            "neighborhood": {"required": False},
            "city": {"required": False},
            "state": {"required": False},
            "cep": {"required": False},
            "complement": {"required": False},
            "full_address": {"required": False},
        }

        read_only_fields = (
            "id",
            "full_address",
            "city",
            "state",
        )