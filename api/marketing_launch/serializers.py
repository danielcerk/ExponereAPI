from rest_framework import serializers

from .models import MarketingLaunch

class MarketingLaunchSerializer(serializers.ModelSerializer):

    class Meta:

        model = MarketingLaunch
        fields = '__all__'

        read_only_fieds = [

            'id', 'campaign_marketing',
            'created_at', 'updated_at'

        ]