from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_notification_type', 'get_message_preview', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['message', 'user__username', 'user__email']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Notification', {'fields': ('user', 'message', 'notification_type')}),
        ('Statut', {'fields': ('is_read', 'related_post')}),
        ('Date', {'fields': ('created_at',)}),
    )
    date_hierarchy = 'created_at'
    list_per_page = 50
    
    def get_notification_type(self, obj):
        return obj.get_notification_type_display()
    get_notification_type.short_description = 'Type'
    
    def get_message_preview(self, obj):
        preview = obj.message[:50]
        if len(obj.message) > 50:
            preview += '...'
        return preview
    get_message_preview.short_description = 'Message'
