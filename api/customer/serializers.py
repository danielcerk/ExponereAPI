from rest_framework import serializers

from django.utils.text import slugify
from django.shortcuts import get_object_or_404

import re

from api.customer.models import Customer
from api.address.models import Address
from api.address.serializers import AddressSerializer

class CustomerSerializer(serializers.ModelSerializer):

    full_name = serializers.CharField(read_only=True)
    address = AddressSerializer(required=True)

    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = (
            'id',
            'slug',
            'full_name',
            'session_key',
            'created_at',
            'updated_at'
        )

        extra_kwargs = {

            'session_key': {'required': False},
            "is_active": {'required': False},
            "catalog": {'required': False},
            "cpf_cnpj": {"validators": []},

        }

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

    def validate(self, data):

        first_name = data.get("first_name", getattr(self.instance, "first_name", ""))
        last_name = data.get("last_name", getattr(self.instance, "last_name", ""))

        if not first_name and not last_name:

            raise serializers.ValidationError(
                "Informe pelo menos o nome ou sobrenome."
            )

        return data

    def create(self, validated_data):

        request = self.context.get("request")

        session = request.session

        if not session.session_key:

            session.save()

        address_data = validated_data.pop("address", None)

        first_name = validated_data.get("first_name", "") or ""
        last_name = validated_data.get("last_name", "") or ""

        full_name = f"{first_name} {last_name}".strip()

        validated_data["full_name"] = full_name
        validated_data["slug"] = slugify(full_name)
        validated_data["session_key"] = session.session_key

        cpf_cnpj = validated_data.get("cpf_cnpj")

        customer = None

        if cpf_cnpj:

            customer = Customer.objects.filter(cpf_cnpj=cpf_cnpj).first()

        if address_data:

            address = Address.objects.create(**address_data)

            validated_data["address"] = address

        if customer:

            for attr, value in validated_data.items():

                setattr(customer, attr, value)

            customer.save()

            return customer

        return Customer.objects.create(**validated_data)

    def update(self, instance, validated_data):

        address_data = validated_data.pop("address", None)

        first_name = validated_data.get("first_name", instance.first_name or "")
        last_name = validated_data.get("last_name", instance.last_name or "")

        full_name = f"{first_name} {last_name}".strip()

        validated_data["full_name"] = full_name
        validated_data["slug"] = slugify(full_name)

        for attr, value in validated_data.items():

            setattr(instance, attr, value)

        if address_data:

            if instance.address:

                for attr, value in address_data.items():

                    setattr(instance.address, attr, value)

                instance.address.save()

            else:

                instance.address = Address.objects.create(**address_data)

        instance.save()

        return instance