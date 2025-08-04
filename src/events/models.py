from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

class Event(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='events/')
    date = models.DateTimeField()
    location = models.CharField(max_length=100)
    lieu_gps= models.URLField(max_length=550)
    is_published = models.BooleanField(default=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Utilisation du modèle User personnalisé
        on_delete=models.CASCADE,
        related_name='events'  # Bonne pratique pour les relations
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def can_edit(self, user):
        """Vérifie si l'utilisateur peut modifier cet événement"""
        return user.is_authenticated and (user == self.author or user.role in ['admin', 'moderateur'])
    def __str__(self):
        return self.title
    def __str__(self):
        return self.title
    def is_upcoming(self):
        return self.is_published and self.date >= timezone.now()