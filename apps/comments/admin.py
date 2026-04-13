from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['get_comment_preview', 'author', 'post', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['content', 'author__username', 'post__title']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Commentaire', {'fields': ('post', 'author', 'content')}),
        ('Dates', {'fields': ('created_at', 'updated_at')}),
    )
    date_hierarchy = 'created_at'
    
    def get_comment_preview(self, obj):
        preview = obj.content[:50]
        if len(obj.content) > 50:
            preview += '...'
        return preview
    get_comment_preview.short_description = 'Commentaire'
