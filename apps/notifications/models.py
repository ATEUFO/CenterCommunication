from django.db import models
from django.conf import settings


class Notification(models.Model):
    """Modèle pour les notifications des utilisateurs"""
    NOTIFICATION_TYPES = [
        ('NEW_POST', 'Nouveau post'),
        ('NEW_COMMENT', 'Nouveau commentaire'),
        ('POST_EXPIRING', 'Post expiration'),
        ('SYSTEM', 'Système'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Utilisateur'
    )
    message = models.TextField(
        verbose_name='Message'
    )
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        default='SYSTEM',
        verbose_name='Type de notification'
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name='Lue'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de création'
    )
    related_post = models.ForeignKey(
        'posts.Post',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='related_notifications',
        verbose_name='Publication liée'
    )
    
    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['user', 'is_read']),
        ]
    
    def __str__(self):
        return f"{self.get_notification_type_display()} - {self.user.username}"
    
    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['user', 'is_read']),
        ]
