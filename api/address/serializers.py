from rest_framework import serializers

from .models import Address

from cities_light.models import SubRegion, Region

class AddressSerializer(serializers.ModelSerializer):

    city = serializers.PrimaryKeyRelatedField(
        queryset=SubRegion.objects.all(),
        required=False
    )

    state = serializers.PrimaryKeyRelatedField(
        queryset=Region.objects.all(),
        required=False
    )

    class Meta:

        model = Address
        fields = '__all__'

        extra_kwargs = {

            'id': {'required': False},
            'street': {'required': False},
            'neighborhood': {'required': False},
            'cep': {'required': False},
            'complement': {'required': False},
            'full_address': {'required': False}

        }

        read_only_fields = (

            'id', 'full_address'

        )

    def to_internal_value(self, data):

        if isinstance(data.get('state'), Region):

            data['state'] = data['state'].id

        if isinstance(data.get('city'), SubRegion):
            
            data['city'] = data['city'].id

        return super().to_internal_value(data)