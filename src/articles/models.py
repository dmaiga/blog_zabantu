from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify, Truncator
from tinymce.models import HTMLField
from django.utils import timezone
import uuid
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
        ('analyse', 'Analyses'),
        ('article', 'Articles'),
        ('policy', 'Policy Briefs'),
        ('ouvrage', 'Ouvrages'),
        ('rapport', 'Rapports'),
        ('scholar', 'Publication Académique'),
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='article'
    )

    title = models.CharField(max_length=255, verbose_name="Titre")
    subtitle = models.CharField(max_length=500, blank=True, null=True, verbose_name="Sous-titre")
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    authors = models.ManyToManyField(User, related_name='articles', verbose_name="Auteurs")
    content = HTMLField(blank=True, null=True, verbose_name="Contenu")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name="Statut")

    pdf_file = models.FileField(upload_to=article_upload_path, blank=True, null=True, verbose_name="Fichier PDF")
    cover_image = models.ImageField(upload_to='articles/covers/', blank=True, null=True, verbose_name="Image de couverture")

    # Champs pour publications académiques
    publisher = models.CharField(max_length=255, blank=True, null=True, verbose_name="Éditeur")
    journal = models.CharField(max_length=255, blank=True, null=True, verbose_name="Revue")
    publication_date = models.DateField(blank=True, null=True, verbose_name="Date de publication")
    scholar_link = models.URLField(blank=True, null=True, verbose_name="Lien Scholar")
    abstract = models.TextField(blank=True, null=True, verbose_name="Résumé")
    is_academic = models.BooleanField(default=False, verbose_name="Publication académique")

    # Métadonnées SEO
    meta_title = models.CharField(max_length=60, blank=True, verbose_name="Titre SEO")
    meta_description = models.CharField(max_length=160, blank=True, verbose_name="Description SEO")

    # Dates
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    publish_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date de publication programmée",
        help_text="Date à laquelle l'article sera automatiquement publié"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.title

    def is_published(self):
        return self.status == 'published'

    def save(self, *args, **kwargs):
        if not self.meta_title:
            self.meta_title = Truncator(self.title).chars(60)

        if not self.meta_description:
            clean_content = re.sub('<[^<]+?>', '', self.content) if self.content else ''
            self.meta_description = Truncator(clean_content).chars(160)

        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Article.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)
    def get_public_category_display(self):
        """Version publique de la catégorie qui regroupe scholar avec article"""
        if self.category == 'scholar':
            return 'Publication Académique'
        return self.get_category_display()

def guelekan_upload_path(instance, filename):
    return f'guelekan/files/{uuid.uuid4()}_{filename}'










class Guelekan(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Brouillon'),
        ('published', 'Publié'),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    subtitle = models.CharField(max_length=500, blank=True)
    content = HTMLField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    cover_image = models.ImageField(upload_to='guelekan/covers/', blank=True, null=True)
    pdf_file = models.FileField(upload_to=guelekan_upload_path, blank=True, null=True)

    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publish_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date de publication programmée"
    )
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def is_published(self):
        return self.status == 'published'

    def save(self, *args, **kwargs):
        if not self.meta_title:
            self.meta_title = Truncator(self.title).chars(60)
        if not self.meta_description:
            clean_content = re.sub('<[^<]+?>', '', self.content)
            self.meta_description = Truncator(clean_content).chars(160)
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Guelekan.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
