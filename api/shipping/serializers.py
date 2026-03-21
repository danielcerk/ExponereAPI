from rest_framework import serializers

from .models import Carrier, ShippingStatus

class CarrierSerializer(serializers.ModelSerializer):

    class Meta:

        models = Carrier
        fields = '__all__'

class ShippingStatus(serializers.ModelSerializer):

    class Meta:

        models = ShippingStatus
        fields = '__all__'