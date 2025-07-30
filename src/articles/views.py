from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Article
from .forms import ArticleForm
from django.utils.text import slugify
from datetime import datetime

# Générateur de slug unique
def generate_unique_slug(title):
    base_slug = slugify(title)
    slug = base_slug
    i = 1
    while Article.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{i}"
        i += 1
    return slug

#  Créer un nouvel article
@login_required
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.slug = generate_unique_slug(article.title)
            article.save()
            return redirect('article_detail', slug=article.slug)
    else:
        form = ArticleForm()
    return render(request, 'articles/article_update.html', {'form': form})

#  Liste des articles de l'utilisateur connecté
@login_required
def article_list(request):
    articles = Article.objects.filter(author=request.user)
    return render(request, 'articles/article_list.html', {'articles': articles})

#  Voir le détail d'un article
@login_required
def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, author=request.user)
    return render(request, 'articles/article_detail.html', {'article': article})

#  Modifier un article
@login_required
def article_update(request, slug):
    article = get_object_or_404(Article, slug=slug, author=request.user)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_detail', slug=article.slug)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'articles/article_update.html', {'form': form, 'is_edit': True})
