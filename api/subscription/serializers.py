from rest_framework import serializers

from .models import Plan

class PlanSerializer(serializers.Serializer):

    class Meta:

        model = Plan
        fields = '__all__'

class CheckoutSessionSerializer(serializers.Serializer):

    price_lookup_key = serializers.CharField(required=True)

class CheckoutSessionResponseSerializer(serializers.Serializer):
    
    checkout_url = serializers.URLField()
    session_id = serializers.CharField()