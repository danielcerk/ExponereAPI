from rest_framework import serializers

from .models import NF

class NFSerializer(serializers.ModelSerializer):

    class Meta:

        model = NF
        fields = '__all__'