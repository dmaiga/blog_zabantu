from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Article
from .forms import ArticleForm
from django.utils.text import slugify
from datetime import datetime
from .media_library import list_media_files  # Ajoutez cette ligne
from django.core.files.storage import default_storage 

from django.contrib import messages
from django.utils import timezone
from django.db.models import Case, When, Value, CharField

# Générateur de slug unique
def generate_unique_slug(title):
    base_slug = slugify(title)
    slug = base_slug
    i = 1
    while Article.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{i}"
        i += 1
    return slug
# articles/views.py (ajouter)
@login_required
def media_library(request):
    media_files = list_media_files()
    return render(request, 'articles/media_library.html', {'media_files': media_files})

@login_required
def unpublish_article(request, slug):
    """Dépublier un article (retour à brouillon)"""
    article = get_object_or_404(Article, slug=slug, author=request.user)
    
    if request.method == 'POST':
        article.status = 'draft'
        article.save()
        messages.success(request, "L'article a été retourné à l'état de brouillon")
        return redirect('article_detail', slug=article.slug)
    
    return render(request, 'articles/unpublish_confirm.html', {'article': article})

@login_required
def publish_article(request, slug):
    """Action spécifique pour publier"""
    article = get_object_or_404(Article, slug=slug, author=request.user)
    
    if request.method == 'POST':
        # Gère les différents cas de publication
        if 'publish_now' in request.POST:
            article.status = 'published'
            article.publish_at = None
        elif 'schedule' in request.POST:
            article.status = 'draft'  # Reste brouillon jusqu'à la date
            article.publish_at = request.POST.get('publish_at')
        
        article.save()
        return redirect('article_detail', slug=article.slug)
    
    return render(request, 'articles/publish_confirm.html', {'article': article})


#  Créer un nouvel article
@login_required
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.status = 'draft'  # Toujours brouillon par défaut
            article.slug = generate_unique_slug(article.title)
            article.save()
            return redirect('article_detail', slug=article.slug)
    else:
        form = ArticleForm()
    return render(request, 'articles/article_update.html', {'form': form})

#  Liste des articles de l'utilisateur connecté
# Dans views.py
@login_required
def article_list(request):
    articles = Article.objects.filter(author=request.user).annotate(
        real_status=Case(
            When(status='published', publish_at__gt=timezone.now(), then=Value('planned')),
            When(status='published', then=Value('published')),
            default=Value('draft'),
            output_field=CharField()
        )
    ).order_by('-created_at')
    
    return render(request, 'articles/article_list.html', {
        'articles': articles,
        'status_classes': {
            'draft': 'text-warning',
            'published': 'text-success',
            'planned': 'text-info'
        }
    })
#  Voir le détail d'un article
@login_required
def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, author=request.user)
    return render(request, 'articles/article_detail.html', {'article': article})

#  Modifier un article
@login_required
def article_update(request, slug):
    article = get_object_or_404(Article, slug=slug, author=request.user)
    
    if article.is_published and not request.user.is_superuser:
        messages.error(request, "Les articles publiés ne peuvent plus être modifiés")
        return redirect('article_detail', slug=article.slug)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_detail', slug=article.slug)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'articles/article_update.html', {'form': form, 'is_edit': True})
