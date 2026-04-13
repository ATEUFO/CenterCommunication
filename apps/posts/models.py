from django.db import models
from django.conf import settings
from django.utils import timezone


class Post(models.Model):
    """Modèle pour représenter une publication sur le babillard"""
    TYPE_CHOICES = [
        ('GLOBAL', 'Globale'),
        ('CLASS', 'Classe'),
        ('PERSONAL', 'Personnel'),
    ]
    
    title = models.CharField(
        max_length=200,
        verbose_name='Titre'
    )
    content = models.TextField(
        verbose_name='Contenu'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Auteur'
    )
    post_type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default='GLOBAL',
        verbose_name='Type de publication'
    )
    classroom = models.ForeignKey(
        'academic.Classroom',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='Classe',
        help_text='À remplir si le type est "Classe"'
    )
    target_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='personal_posts',
        verbose_name='Utilisateur cible',
        help_text='À remplir si le type est "Personnel"'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Date d\'expiration'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Actif'
    )
    
    class Meta:
        verbose_name = 'Publication'
        verbose_name_plural = 'Publications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_active']),
            models.Index(fields=['post_type']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.author.username}"
    
    def is_expired(self):
        """Vérifie si le post est expiré"""
        if self.expires_at and self.expires_at < timezone.now():
            return True
        return False
    
    def save(self, *args, **kwargs):
        """Met à jour le statut is_active si expiration atteinte"""
        if self.is_expired():
            self.is_active = False
        super().save(*args, **kwargs)


class ArchivedPost(models.Model):
    """Modèle pour archiver les publications expirées"""
    original_post_id = models.BigIntegerField(
        verbose_name='ID du post original'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Titre'
    )
    content = models.TextField(
        verbose_name='Contenu'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='archived_posts',
        verbose_name='Auteur'
    )
    post_type = models.CharField(
        max_length=10,
        verbose_name='Type de publication'
    )
    created_at = models.DateTimeField(verbose_name='Date de création')
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Date d\'expiration'
    )
    archived_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date d\'archivage'
    )
    
    class Meta:
        verbose_name = 'Publication archivée'
        verbose_name_plural = 'Publications archivées'
        ordering = ['-archived_at']
        indexes = [
            models.Index(fields=['-archived_at']),
        ]
    
    def __str__(self):
        return f"[ARCHIVÉ] {self.title}"


def post_media_path(instance, filename):
    """Génère le chemin de stockage pour les médias de publication"""
    return f'posts/{instance.post.id}/{filename}'


class PostMedia(models.Model):
    """Modèle pour représenter les fichiers joints à une publication"""
    MEDIA_TYPES = [
        ('IMAGE', 'Image'),
        ('PDF', 'Document PDF'),
        ('VIDEO', 'Vidéo'),
        ('OTHER', 'Autre'),
    ]
    
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='media',
        verbose_name='Publication'
    )
    file = models.FileField(
        upload_to=post_media_path,
        verbose_name='Fichier'
    )
    media_type = models.CharField(
        max_length=10,
        choices=MEDIA_TYPES,
        default='OTHER',
        verbose_name='Type de média'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Média de publication'
        verbose_name_plural = 'Médias de publication'
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.get_media_type_display()} pour {self.post.title}"

