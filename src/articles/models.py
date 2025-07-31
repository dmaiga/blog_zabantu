from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify,Truncator
from tinymce.models import HTMLField
import uuid
from django.conf import settings

from django.utils import timezone
from django.core.exceptions import ValidationError

import re


User = get_user_model()

def article_upload_path(instance, filename):
    return f'articles/{uuid.uuid4()}_{filename}'

class Article(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Brouillon'),
        ('published', 'Publié'),
    )
    
    CATEGORY_CHOICES = (
        ('seminaire', 'Séminaire Guelekan'),
        ('analyse', 'Analyse'),
        ('publication', 'Publication'),
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='publication'
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='articles')
    content = HTMLField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publish_at = models.DateTimeField(null=True, blank=True, verbose_name="Planifier la publication")
    
    # Upload PDF version (facultatif)
    pdf_file = models.FileField(upload_to=article_upload_path, blank=True, null=True)
    cover_image = models.ImageField(upload_to='articles/covers/', blank=True, null=True)
    #meta
    meta_title = models.CharField(max_length=60, blank=True, verbose_name="Titre SEO")
    meta_description = models.CharField(max_length=160, blank=True, verbose_name="Description SEO")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    def is_published(self):
        if self.status != 'published':
            return False
        if self.publish_at and self.publish_at > timezone.now():
            return False
        return True
    
    def get_status_display(self):
        """Surcharge pour afficher le statut réel"""
        status = self.publication_status
        return {
            'planned': "Planifié",
            'published': "Publié",
            'draft': "Brouillon"
        }.get(status, status)
    
    @property
    def is_planned(self):
        """Vérifie si l'article est planifié"""
        return self.publication_status == 'planned'
    
    def save(self, *args, **kwargs):
        if not self.meta_title:
            self.meta_title = Truncator(self.title).chars(60)  # Bonne syntaxe
    
        if not self.meta_description:
             clean_content = re.sub('<[^<]+?>', '', self.content)
             self.meta_description = Truncator(clean_content).chars(160)
        # Génération du slug unique si vide
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Article.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def publication_status(self):
            """Retourne le statut réel en tenant compte de la planification"""
            now = timezone.now()
            if self.status == 'published':
                if self.publish_at and self.publish_at > now:
                    return 'planned'
                return 'published'
            return 'draft'
        
    def clean(self):
            """Validation supplémentaire"""
            if self.status == 'published' and self.publish_at and self.publish_at > timezone.now():
                raise ValidationError(
                    "Vous ne pouvez pas mettre un article en 'publié' avec une date future. "
                    "Utilisez le statut 'brouillon' et planifiez la date."
                )   