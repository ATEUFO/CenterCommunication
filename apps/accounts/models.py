from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('STUDENT', 'Étudiant'),
        ('TEACHER', 'Enseignant'),
        ('ADMIN', 'Administrateur'),
    ]
    
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='STUDENT',
        verbose_name='Rôle'
    )
    is_active = models.BooleanField(default=True, verbose_name='Actif')
    
    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"


class AuditLog(models.Model):
    """Modèle pour enregistrer les actions administratives"""
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='audit_logs',
        verbose_name='Administrateur'
    )
    action = models.CharField(
        max_length=255,
        verbose_name='Action'
    )
    target = models.CharField(
        max_length=255,
        verbose_name='Cible',
        help_text='Objet ou utilisateur affecté'
    )
    details = models.TextField(
        blank=True,
        verbose_name='Détails'
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name='Adresse IP'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Journal d\'audit'
        verbose_name_plural = 'Journaux d\'audit'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.created_at} - {self.user} - {self.action}"

