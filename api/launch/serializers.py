import re

from rest_framework import serializers

from .models import Launch


class LaunchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Launch
        fields = "__all__"

        extra_kwargs = {
            "whatsapp": {"required": True},
        }

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_whatsapp(self, value):

        value = re.sub(r"\D", "", value)

        if not value.startswith("+55"):

            value = f"+55{value}"

        if len(value) not in (13, 14):
            raise serializers.ValidationError(
                "Informe um WhatsApp válido com DDD."
            )

        return f"{value}"