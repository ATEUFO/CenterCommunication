from rest_framework import serializers
from .models import Post, ArchivedPost


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    classroom_name = serializers.CharField(source='classroom.name', read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'post_type', 'classroom', 'classroom_name', 'target_user', 'created_at', 'expires_at', 'is_active']
        read_only_fields = ['id', 'created_at', 'author']


class PostDetailSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    comment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'post_type', 'classroom', 'target_user', 'created_at', 'expires_at', 'is_active', 'comment_count']
        read_only_fields = ['id', 'created_at', 'author']
    
    def get_comment_count(self, obj):
        return obj.comments.count()


class ArchivedPostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    
    class Meta:
        model = ArchivedPost
        fields = ['id', 'title', 'content', 'author', 'post_type', 'created_at', 'expires_at', 'archived_at']
        read_only_fields = ['id', 'archived_at']
