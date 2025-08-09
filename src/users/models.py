from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.urls import reverse

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', _('Administrateur')),
        ('moderateur', _('Modérateur')),
        ('membre', _('Membre')),
    ]
    
    # Validateur pour le numéro de téléphone
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=_("Le numéro doit être au format: '+999999999'. Jusqu'à 15 chiffres.")
    )
    
    # Identité
    nom = models.CharField(_('nom'), max_length=100, blank=False)
    prenom = models.CharField(_('prénom'), max_length=100, blank=False)
    
    # Rôle et statut
    role = models.CharField(
        _('rôle'), 
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='membre'
    )
    date_started = models.DateField(_('date de début'), null=True, blank=True)
    is_active = models.BooleanField(_('actif'), default=True)
    
    # Contact
    email = models.EmailField(_('email'), unique=True, blank=False)
    phone_number = models.CharField(
        _('téléphone'), 
        max_length=20, 
        validators=[phone_regex],
        blank=True, 
        null=True
    )
    profile_picture = models.ImageField(
        _('photo de profil'),
        upload_to='profiles/%Y/%m/%d/',
        blank=True, 
        null=True,
        default='profiles/default.png'
    )
    
    # Profession
    bio = models.TextField(_('biographie'), blank=True, null=True)
    job_title = models.CharField(_('poste'), max_length=100, blank=True, null=True)
    department = models.CharField(_('département'), max_length=100, blank=True, null=True)
    
    # Réseaux sociaux
    social_facebook = models.URLField(_('Facebook'), blank=True, null=True)
    social_linkedin = models.URLField(_('LinkedIn'), blank=True, null=True)
    social_twitter = models.URLField(_('Twitter'), blank=True, null=True)
    social_instagram = models.URLField(_('Instagram'), blank=True, null=True)
    
    # Métadonnées
    created_at = models.DateTimeField(_('créé le'), auto_now_add=True)
    updated_at = models.DateTimeField(_('modifié le'), auto_now=True)
    
    class Meta:
        verbose_name = _('utilisateur')
        verbose_name_plural = _('utilisateurs')
        ordering = ['nom', 'prenom']
    
    REQUIRED_FIELDS = ['nom', 'prenom', 'email']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
    
    def get_full_name(self):
        """Retourne le nom complet."""
        return f"{self.prenom} {self.nom}".strip()
    
    def get_short_name(self):
        """Retourne le prénom."""
        return self.prenom
    
    def get_profile_picture(self):
        """Retourne l'URL de la photo de profil ou une image par défaut."""
        if self.profile_picture:
            return self.profile_picture.url
        return '/static/images/default-profile.png'
    
    def get_social_links(self):
        """Retourne les liens sociaux sous forme de dictionnaire."""
        return {
            'facebook': self.social_facebook,
            'linkedin': self.social_linkedin,
            'twitter': self.social_twitter,
            'instagram': self.social_instagram
        }
    
    def get_public_profile(self):
        """Retourne l'URL publique du profil du membre."""
        return reverse('membre_detail', args=[self.pk])
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    @property
    def is_moderator(self):
        return self.role == 'moderateur'
    
    def save(self, *args, **kwargs):
        # Nettoyage des champs
        self.email = self.email.lower().strip()
        self.nom = self.nom.strip().upper()
        self.prenom = self.prenom.strip().title()
        super().save(*args, **kwargs)