from django.shortcuts import render, get_object_or_404
from articles.models import Article

def article_list_public(request):
    articles = Article.objects.filter(status='published').order_by('-created_at')
    return render(request, 'site_web/public_article_list.html', {'articles': articles})

def article_detail_public(request, slug):
    article = get_object_or_404(Article, slug=slug, status='published')
    return render(request, 'site_web/public_article_detail.html', {'article': article})
