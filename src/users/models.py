from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('moderateur', 'Modérateur'),
        ('membre', 'Membre'),
    ]
    
    #Role et statut
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='membre')
    date_started = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    #Identite et contact
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True, default='profiles/default.png')
    #Presentation
    bio = models.TextField(blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    #linkedin
    social_facebook = models.URLField(blank=True, null=True)
    social_linkedin = models.URLField(blank=True, null=True)
    social_twitter = models.URLField(blank=True, null=True)
    #Metadonne
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    
    @property
    def has_admin_rights(self):
        return self.role in ['admin', 'moderateur']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
