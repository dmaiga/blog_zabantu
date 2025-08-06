from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class ExternalParticipant(models.Model):
    PARTICIPANT_TYPE_CHOICES = [
        ('moderator', 'Modérateur'),
        ('speaker', 'Intervenant'),
        ('trainer', 'Formateur'),
    ]
    
    first_name = models.CharField(max_length=100, verbose_name="Prénom")
    last_name = models.CharField(max_length=100, verbose_name="Nom")
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Téléphone")
    organization = models.CharField(max_length=200, blank=True, null=True, verbose_name="Organisation")
    bio = models.TextField(blank=True, null=True, verbose_name="Biographie")
    participant_type = models.CharField(
        max_length=20,
        choices=PARTICIPANT_TYPE_CHOICES,
        verbose_name="Type de participant"
    )
    photo = models.ImageField(
        upload_to='participants/', 
        blank=True, 
        null=True,
        verbose_name="Photo"
    )
    linkedin = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Participant externe"
        verbose_name_plural = "Participants externes"
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_participant_type_display()})"
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ('conference', 'Conférence'),
        ('formation', 'Formation'),
        ('seminaire', 'Séminaire'),
        ('autre', 'Autre'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Titre")
    content = models.TextField(verbose_name="Contenu")
    image = models.ImageField(upload_to='events/', verbose_name="Image")
    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPE_CHOICES,
        default='seminaire',
        verbose_name="Type d'événement"
    )
    date = models.DateTimeField(verbose_name="Date et heure de début")
    end_date = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name="Date et heure de fin"
    )
    location = models.CharField(max_length=100, verbose_name="Lieu")
    lieu_gps = models.URLField(
        max_length=550, 
        blank=True, 
        null=True,
        verbose_name="Lien GPS"
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name="Publié"
    )
    
    # Relations
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='authored_events',
        verbose_name="Auteur"
    )
    
    moderators = models.ManyToManyField(
        ExternalParticipant,
        limit_choices_to={'participant_type': 'moderator'},
        blank=True,
        related_name='moderated_events',
        verbose_name="Modérateurs"
    )
    
    speakers = models.ManyToManyField(
        ExternalParticipant,
        limit_choices_to={'participant_type': 'speaker'},
        blank=True,
        related_name='speaker_events',
        verbose_name="Intervenants"
    )
    
    trainers = models.ManyToManyField(
        ExternalParticipant,
        limit_choices_to={'participant_type': 'trainer'},
        blank=True,
        related_name='training_events',
        verbose_name="Formateurs"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def is_upcoming(self):
        """Vérifie si l'événement est à venir"""
        return self.is_published and self.date >= timezone.now()
    
    def get_event_duration(self):
        """Retourne la durée formatée de l'événement"""
        if self.end_date:
            return f"{self.date.strftime('%d/%m/%Y %H:%M')} - {self.end_date.strftime('%d/%m/%Y %H:%M')}"
        return self.date.strftime('%d/%m/%Y %H:%M')
    
    class Meta:
        ordering = ['-date']
        verbose_name = "Événement"
        verbose_name_plural = "Événements"