from rest_framework import serializers

from .models import MarketingLaunch

import re

class MarketingLaunchSerializer(serializers.ModelSerializer):

    class Meta:

        model = MarketingLaunch
        fields = '__all__'

        read_only_fieds = [

            'id', 'campaign_marketing',
            'created_at', 'updated_at'

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