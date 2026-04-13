from django.db import models
from django.conf import settings


class Establishment(models.Model):
    """Modèle pour représenter un établissement scolaire"""
    name = models.CharField(
        max_length=255,
        verbose_name='Nom de l\'établissement',
        unique=True
    )
    address = models.CharField(
        max_length=500,
        verbose_name='Adresse'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Établissement'
        verbose_name_plural = 'Établissements'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Classroom(models.Model):
    """Modèle pour représenter une classe"""
    name = models.CharField(
        max_length=100,
        verbose_name='Nom de la classe'
    )
    establishment = models.ForeignKey(
        Establishment,
        on_delete=models.CASCADE,
        related_name='classrooms',
        verbose_name='Établissement'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Classe'
        verbose_name_plural = 'Classes'
        unique_together = ('name', 'establishment')
        ordering = ['establishment', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.establishment.name})"


class Student(models.Model):
    """Modèle pour représenter un étudiant"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile',
        verbose_name='Utilisateur'
    )
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
        verbose_name='Classe'
    )
    matricule = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Matricule'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Étudiant'
        verbose_name_plural = 'Étudiants'
        ordering = ['classroom', 'user__username']
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.matricule})"


class Teacher(models.Model):
    """Modèle pour représenter un enseignant"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teacher_profile',
        verbose_name='Utilisateur'
    )
    classrooms = models.ManyToManyField(
        Classroom,
        related_name='teachers',
        verbose_name='Classes',
        blank=True
    )
    speciality = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Spécialité'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Enseignant'
        verbose_name_plural = 'Enseignants'
        ordering = ['user__username']
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.speciality or 'Non défini'})"
