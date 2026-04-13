from django.contrib import admin
from django.utils.html import format_html
from .models import Post, ArchivedPost


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'get_post_type', 'is_active_color', 'created_at', 'expires_at']
    list_filter = ['post_type', 'is_active', 'created_at', 'expires_at']
    search_fields = ['title', 'content', 'author__username']
    readonly_fields = ['created_at', 'is_expired']
    fieldsets = (
        ('Publication', {'fields': ('title', 'content', 'author')}),
        ('Ciblage', {'fields': ('post_type', 'classroom', 'target_user')}),
        ('Durée', {'fields': ('created_at', 'expires_at', 'is_expired')}),
        ('Statut', {'fields': ('is_active',)}),
    )
    date_hierarchy = 'created_at'
    
    def get_post_type(self, obj):
        return obj.get_post_type_display()
    get_post_type.short_description = 'Type'
    
    def is_active_color(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="color: green;">&#9679;</span> Actif'
            )
        else:
            return format_html(
                '<span style="color: red;">&#9679;</span> Inactif'
            )
    is_active_color.short_description = 'Statut'


@admin.register(ArchivedPost)
class ArchivedPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'post_type', 'archived_at', 'expires_at']
    list_filter = ['post_type', 'archived_at', 'expires_at']
    search_fields = ['title', 'content', 'author__username']
    readonly_fields = ['original_post_id', 'created_at', 'archived_at']
    fieldsets = (
        ('Publication archivée', {'fields': ('title', 'content', 'author', 'original_post_id')}),
        ('Informations', {'fields': ('post_type', 'created_at', 'expires_at', 'archived_at')}),
    )
    date_hierarchy = 'archived_at'
    can_delete = True
