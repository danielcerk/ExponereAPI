from rest_framework import serializers

from .models import MetaPixel, TagManager, GA4

class MetaPixelSerializer(serializers.ModelSerializer):

    class Meta:

        model = MetaPixel
        fields = '__all__'

        read_only_fields = [
            'pk'
        ]

class TagManagerSerializer(serializers.ModelSerializer):

    class Meta:

        model = TagManager
        fields = '__all__'

        read_only_fields = [
            'pk'
        ]

class GA4Serializer(serializers.ModelSerializer):

    class Meta:

        model = GA4
        fields = '__all__'

        read_only_fields = [
            'pk'
        ]