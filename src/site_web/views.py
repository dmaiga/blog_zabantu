from django.shortcuts import render, get_object_or_404
from articles.models import Article

def public_article_list(request):
    type_filter = request.GET.get('type')
    articles = Article.objects.filter(status='published')

    if type_filter in ['seminaire', 'analyse', 'publication']:
        articles = articles.filter(category=type_filter)

    return render(request, 'site_web/public_article_list.html', {
        'articles': articles,
        'type_filter': type_filter
    })

def public_article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, status='published')
    return render(request, 'site_web/public_article_detail.html', {'article': article})
