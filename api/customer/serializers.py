from rest_framework import serializers
from django.utils.text import slugify
import re

from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):

    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = (
            'id',
            'slug',
            'full_name',
            'created_at',
            'updated_at'
        )

    def validate_first_name(self, value):

        if value:

            value = value.strip()

            if len(value) < 2:

                raise serializers.ValidationError("Nome muito curto.")

        return value

    def validate_last_name(self, value):

        if value:

            value = value.strip()

        return value

    def validate_whatsapp(self, value):

        if value:

            value = value.strip()

            pattern = r'^\+?55\d{10,11}$'

            if not re.match(pattern, value):

                raise serializers.ValidationError(
                    "Número inválido. Use formato +5511999999999."
                )
            
        return value

    def validate_cpf_cnpj(self, value):

        if value:

            value = value.strip()

            if Customer.objects.filter(cpf_cnpj=value).exclude(
                pk=self.instance.pk if self.instance else None
            ).exists():
                
                raise serializers.ValidationError(
                    "CPF/CNPJ já cadastrado."
                )
            
        return value

    def validate(self, data):

        first_name = data.get("first_name", getattr(self.instance, "first_name", ""))
        last_name = data.get("last_name", getattr(self.instance, "last_name", ""))

        if not first_name and not last_name:

            raise serializers.ValidationError(
                "Informe pelo menos o nome ou sobrenome."
            )

        return data

    def create(self, validated_data):

        first_name = validated_data.get("first_name", "") or ""
        last_name = validated_data.get("last_name", "") or ""

        full_name = f"{first_name} {last_name}".strip()

        validated_data["full_name"] = full_name
        validated_data["slug"] = slugify(full_name)

        return super().create(validated_data)

    def update(self, instance, validated_data):

        first_name = validated_data.get("first_name", instance.first_name or "")
        last_name = validated_data.get("last_name", instance.last_name or "")

        full_name = f"{first_name} {last_name}".strip()

        validated_data["full_name"] = full_name
        validated_data["slug"] = slugify(full_name)

        return super().update(instance, validated_data)