from rest_framework import serializers

from .models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:

        model = Feedback
        fields = '__all__'

        read_olny_fields = [

            'id', 'user', 'created_at', 'updated_at'

        ]