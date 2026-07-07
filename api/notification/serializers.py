from rest_framework import serializers

from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):

    class Meta:

        model = Notification
        fields = '__all__'

        read_only_fields = (

            'id', 'catalog', 'user',
            'type_notification', 'title',
            'message', 'action_url', 'payload',
            'is_read', 'readt_at', 'created_at', # Funções de is_read estão em standby
            'updated_at'

        )