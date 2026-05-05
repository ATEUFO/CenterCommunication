from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.urls import reverse
import os


class HomeAPIView(APIView):
    """API d'accueil - Affiche les informations du projet"""
    permission_classes = [AllowAny]  # Permettre l'accès sans authentification
    
    def get(self, request):
        # Construire les URLs dynamiquement
        protocol = 'https' if request.is_secure() else 'http'
        host = request.get_host()  # Inclut le port automatiquement
        
        return Response({
            'message': '🎓 Bienvenue sur CouCou',
            'description': 'Babillard intelligent d\'établissement scolaire',
            'version': '1.0.0',
            'server': {
                'protocol': protocol,
                'host': host,
                'environment': 'development' if os.environ.get('DEBUG', 'True') == 'True' else 'production',
            },
            'endpoints': {
                'admin': '/admin/',
                'api_auth_login': '/api-auth/login/',
                'api_auth_logout': '/api-auth/logout/',
                'users': '/api/v1/auth/users/',
                'establishments': '/api/v1/academic/establishments/',
                'classrooms': '/api/v1/academic/classrooms/',
                'students': '/api/v1/academic/students/',
                'teachers': '/api/v1/academic/teachers/',
                'posts': '/api/v1/posts/posts/',
                'archived_posts': '/api/v1/posts/archived-posts/',
                'comments': '/api/v1/comments/comments/',
                'notifications': '/api/v1/notifications/notifications/',
            },
            'status': 'online ✓',
            'help': {
                'get_started': 'Visitez /admin/ pour l\'interface administration',
                'api_docs': 'Documentation API disponible sur chaque endpoint',
                'test': 'Utilisez les credentials test_users pour accéder aux endpoints',
            }
        })
