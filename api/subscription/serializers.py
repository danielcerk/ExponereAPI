from rest_framework import serializers

from .models import *

class PlanSerializer(serializers.ModelSerializer):

    class Meta:

        model = Plan
        fields = '__all__'

class CheckoutSessionSerializer(serializers.Serializer):

    price_lookup_key = serializers.CharField(required=True)

class CheckoutSessionResponseSerializer(serializers.Serializer):
    
    checkout_url = serializers.URLField()
    session_id = serializers.CharField()

class UserSubscriptionSerializer(serializers.ModelSerializer):

    plan = serializers.SerializerMethodField()

    class Meta:
        model = CheckoutSessionRecord
        fields = [
            'status',
            'has_access',
            'is_completed',
            'plan_start_date',
            'plan_end_date',
            'amount_total',
            'currency',
            'plan',
        ]

    def get_plan(self, obj):

        if not obj.plan:
            return None

        return {
            'id': obj.plan.id,
            'name': obj.plan.name,
            'lookup_key_plan': obj.plan.lookup_key_plan,
            'description': obj.plan.description,
            'price': obj.plan.price,
            'currency': obj.plan.currency,
            'duration': obj.plan.duration,
            'is_active': obj.plan.is_active,
        }