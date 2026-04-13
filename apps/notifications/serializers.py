from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'notification_type', 'is_read', 'created_at', 'related_post']
        read_only_fields = ['id', 'created_at', 'user']
