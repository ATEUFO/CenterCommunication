from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Comment
from .serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['content', 'author__username']
    filterset_fields = ['post']
    
    def get_queryset(self):
        return Comment.objects.select_related('post', 'author').order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=False, methods=['get'])
    def by_post(self, request):
        post_id = request.query_params.get('post_id')
        if post_id:
            comments = Comment.objects.filter(post_id=post_id).order_by('-created_at')
            serializer = self.get_serializer(comments, many=True)
            return Response(serializer.data)
        return Response({'detail': 'post_id parameter required'}, status=400)
