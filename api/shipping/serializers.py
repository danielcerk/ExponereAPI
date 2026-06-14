from rest_framework import serializers
from django.utils.text import slugify

from .models import Carrier, ShippingStatus

class CarrierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Carrier
        fields = '__all__'
        read_only_fields = ('id', 'slug', 'created_at', 'updated_at')

    def validate_name(self, value):

        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError("O nome deve ter pelo menos 2 caracteres.")

        return value

    def validate(self, data):

        name = data.get("name")

        if Carrier.objects.filter(name__iexact=name).exclude(
            pk=self.instance.pk if self.instance else None
        ).exists():
            raise serializers.ValidationError({
                "name": "Já existe uma transportadora com esse nome."
            })

        return data

    def create(self, validated_data):

        validated_data["name"] = validated_data["name"].strip()

        return super().create(validated_data)

    def update(self, instance, validated_data):

        if "name" in validated_data:

            validated_data["name"] = validated_data["name"].strip()

        return super().update(instance, validated_data)

class ShippingStatusSerializer(serializers.ModelSerializer):

    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True
    )

    class Meta:
        model = ShippingStatus
        fields = '__all__'
        read_only_fields = (
            'id',
            'created_at',
            'updated_at',
            'status_display'
        )

    def validate_tracking_code(self, value):

        value = value.strip()

        if len(value) < 5:
            raise serializers.ValidationError("Código de rastreio inválido.")

        return value

    def validate(self, data):

        tracking_code = data.get("tracking_code")
        order = data.get("order")

        if ShippingStatus.objects.filter(
            tracking_code=tracking_code,
            order=order,
            status=data.get("status")
        ).exclude(
            pk=self.instance.pk if self.instance else None
        ).exists():
            raise serializers.ValidationError(
                "Esse status já foi registrado para este pedido."
            )

        return data

    def create(self, validated_data):

        if "tracking_code" in validated_data:

            validated_data["tracking_code"] = validated_data["tracking_code"].strip().upper()

        return super().create(validated_data)

    def update(self, instance, validated_data):

        if "tracking_code" in validated_data:

            validated_data["tracking_code"] = validated_data["tracking_code"].strip().upper()

        return super().update(instance, validated_data)