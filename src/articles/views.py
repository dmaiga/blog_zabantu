from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify
from django.utils import timezone
from django.db.models import Value, CharField
from .models import Article,Guelekan
from .forms import ArticleForm,GuelekanForm
from .media_library import list_media_files  



# Générateur de slug unique
def generate_unique_slug(title):
    base_slug = slugify(title)
    slug = base_slug
    i = 1
    while Article.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{i}"
        i += 1
    return slug

# 📁 Media Library
@login_required
def media_library(request):
    media_files = list_media_files()
    return render(request, 'articles/media_library.html', {'media_files': media_files})

# 📝 Créer un article
@login_required
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.slug = generate_unique_slug(article.title)
            article.status = 'draft'
            article.save()
            form.save_m2m()
            return redirect('article_detail', slug=article.slug)
    else:
        form = ArticleForm()
    return render(request, 'articles/article_update.html', {'form': form})

# ✏️ Modifier un article
@login_required
def article_update(request, slug):
    article = get_object_or_404(Article, slug=slug)

    if article.is_published() and not request.user.is_superuser:
        messages.error(request, "Les articles publiés ne peuvent plus être modifiés.")
        return redirect('article_detail', slug=article.slug)

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()  # Sauvegarde tout en une fois (y compris les relations ManyToMany)
            messages.success(request, "L'article a été mis à jour avec succès.")
            return redirect('article_detail', slug=article.slug)
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = ArticleForm(instance=article)
    
    return render(request, 'articles/article_update.html', {'form': form, 'is_edit': True})
# 📃 Liste des articles
# views.py
from django.db.models import Q
from datetime import datetime

@login_required
def article_list(request):
    articles = Article.objects.all().order_by('-created_at')
    
    # Filtrage
    category = request.GET.get('category')
    status = request.GET.get('status')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    if category:
        articles = articles.filter(category=category)
    
    if status:
        articles = articles.filter(status=status)
    
    if date_from:
        try:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
            articles = articles.filter(created_at__date__gte=date_from)
        except ValueError:
            pass
    
    if date_to:
        try:
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
            articles = articles.filter(created_at__date__lte=date_to)
        except ValueError:
            pass
    
    return render(request, 'articles/article_list.html', {
        'articles': articles,
        'categories': Article.CATEGORY_CHOICES,
        'status_choices': Article.STATUS_CHOICES,
        'selected_category': category,
        'selected_status': status,
        'date_from': date_from,
        'date_to': date_to,
    })

# 🔍 Détail d'un article
@login_required
def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request, 'articles/article_detail.html', {'article': article})

# 🗑️ Supprimer un article
@login_required
def article_delete(request, slug):
    article = get_object_or_404(Article, slug=slug)

    if request.method == 'POST':
        article.delete()
        messages.success(request, "L'article a été supprimé avec succès.")
        return redirect('article_list')

    return render(request, 'articles/article_confirm_delete.html', {'article': article})


@login_required
def publish_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if not article.is_published():
        article.status = 'published'
        article.save()
        messages.success(request, f"L'article « {article.title} » a été publié.")
    return redirect('article_detail', slug=slug)  # Redirige vers le détail de l'article

@login_required
def unpublish_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if article.is_published():
        article.status = 'draft'
        article.save()
        messages.warning(request, f"L'article « {article.title} » a été dépublié.")
    return redirect('article_detail', slug=slug)  # Redirige vers le détail de l'article


#
#---------------------------------------------------------
#                              Guelekan    
#________________________________________________________
#

def generate_guelekan_slug(title):
    base_slug = slugify(title)
    slug = base_slug
    i = 1
    while Guelekan.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{i}"
        i += 1
    return slug

@login_required
def guelekan_list(request):
    guelekans = Guelekan.objects.all().order_by('-created_at')
    return render(request, 'articles/guelekan_list.html', {
        'guelekans': guelekans,
        'status_classes': {
            'draft': 'text-warning',
            'published': 'text-success',
        }
    })

@login_required
def guelekan_create(request):
    if request.method == 'POST':
        form = GuelekanForm(request.POST, request.FILES)
        if form.is_valid():
            guelekan = form.save(commit=False)
            guelekan.slug = generate_guelekan_slug(guelekan.title)
            guelekan.save()
            messages.success(request, "Le Guelekan a été créé avec succès.")
            return redirect('guelekan_detail', slug=guelekan.slug)
    else:
        form = GuelekanForm()
    return render(request, 'articles/guelekan_form.html', {'form': form})

@login_required
def guelekan_update(request, slug):
    guelekan = get_object_or_404(Guelekan, slug=slug)

    if guelekan.is_published() and not request.user.is_superuser:
        messages.error(request, "Les Guelekan publiés ne peuvent plus être modifiés.")
        return redirect('guelekan_detail', slug=guelekan.slug)

    if request.method == 'POST':
        form = GuelekanForm(request.POST, request.FILES, instance=guelekan)
        if form.is_valid():
            form.save()
            messages.success(request, "Le Guelekan a été mis à jour avec succès.")
            return redirect('guelekan_detail', slug=guelekan.slug)
    else:
        form = GuelekanForm(instance=guelekan)
    return render(request, 'articles/guelekan_form.html', {'form': form, 'is_edit': True})

@login_required
def guelekan_detail(request, slug):
    guelekan = get_object_or_404(Guelekan, slug=slug)
    return render(request, 'articles/guelekan_detail.html', {'guelekan': guelekan})

@login_required
def guelekan_delete(request, slug):
    guelekan = get_object_or_404(Guelekan, slug=slug)

    if request.method == 'POST':
        guelekan.delete()
        messages.success(request, "Le Guelekan a été supprimé avec succès.")
        return redirect('guelekan_list')

    return render(request, 'articles/guelekan_confirm_delete.html', {'guelekan': guelekan})

@login_required
def publish_guelekan(request, slug):
    guelekan = get_object_or_404(Guelekan, slug=slug)
    if not guelekan.is_published():
        guelekan.status = 'published'
        guelekan.save()
        messages.success(request, f"Le Guelekan « {guelekan.title} » a été publié.")
    return redirect('guelekan_detail', slug=slug)

@login_required
def unpublish_guelekan(request, slug):
    guelekan = get_object_or_404(Guelekan, slug=slug)
    if guelekan.is_published():
        guelekan.status = 'draft'
        guelekan.save()
        messages.warning(request, f"Le Guelekan « {guelekan.title} » a été dépublié.")
    return redirect('guelekan_detail', slug=slug)