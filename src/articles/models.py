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
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='article'  
    )

    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=500)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    authors = models.ManyToManyField(User, related_name='articles')
    content = HTMLField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    pdf_file = models.FileField(upload_to=article_upload_path, blank=True, null=True)
    cover_image = models.ImageField(upload_to='articles/covers/', blank=True, null=True)

    meta_title = models.CharField(max_length=60, blank=True, verbose_name="Titre SEO")
    meta_description = models.CharField(max_length=160, blank=True, verbose_name="Description SEO")

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
            while Article.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)



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
