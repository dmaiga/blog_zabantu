from django.shortcuts import render, get_object_or_404
from articles.models import Article,Guelekan
from events.models import Event
from django.views.generic import TemplateView
from django.utils import timezone

def public_article_list(request):
    type_filter = request.GET.get('type', None)
    articles = Article.objects.filter(status='published')
    
    # Filtrer par catégorie si spécifié
    if type_filter in ['seminaire', 'analyse', 'publication']:
        articles = articles.filter(category=type_filter)
    
    # Compter les articles par catégorie pour le menu
    categories = {
        'seminaire': articles.filter(category='seminaire').count(),
        'analyse': articles.filter(category='analyse').count(),
        'publication': articles.filter(category='publication').count()
    }
    
    return render(request, 'site_web/public_article_list.html', {
        'articles': articles.order_by('-created_at'),
        'current_filter': type_filter,
        'categories': categories
    })

from django.http import Http404

def public_article_detail(request, slug):
    article = get_object_or_404(
        Article, 
        slug=slug, 
        status='published'
    )
    
    if article.publish_at and article.publish_at > timezone.now():
        raise Http404("Cet article n'est pas encore publié")
    
    authors = article.authors.all()
    
    return render(request, 'site_web/public_article_detail.html', {
        'article': article,
        'authors': authors,
    })



from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from events.models import Event

def public_event_list(request):
    """Liste des événements publics à venir"""
    upcoming_events = Event.objects.filter(
        is_published=True,
        date__gte=timezone.now()
    ).order_by('date')
    
    past_events = Event.objects.filter(
        is_published=True,
        date__lt=timezone.now()
    ).order_by('-date')[:5]  # Limite à 5 événements passés
    
    return render(request, 'site_web/public_event_list.html', {
        'upcoming_events': upcoming_events,
        'past_events': past_events
    })

def public_event_detail(request, pk):
    """Détail d'un événement public"""
    event = get_object_or_404(
        Event, 
        pk=pk,
        is_published=True
    )
    
    # Vérifier si l'événement est passé
    is_past_event = event.date < timezone.now()
    
    return render(request, 'site_web/public_event_detail.html', {
        'event': event,
        'is_past_event': is_past_event
    })

from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone
from articles.models import Article
from events.models import Event

class HomeView(TemplateView):
    template_name = 'site_web/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Derniers articles publiés (toutes catégories)
        context['latest_articles'] = [
            article for article in 
            Article.objects.order_by('-created_at')[:4]
            if article.is_published()
        ]
        
        # Événements à venir
        context['upcoming_events'] = Event.objects.filter(
            is_published=True,
            date__gte=timezone.now()
        ).order_by('date')[:3]
         # Mise en avant spéciale (ex: dernier séminaire)
        context['featured_seminar'] = Guelekan.objects.filter(
            
            status='published'
        ).order_by('-created_at').first()
        
        return context
    

from users.models import CustomUser
from django.shortcuts import render

def public_member_list(request):
    """Liste des membres publics"""
    members = CustomUser.objects.filter(
        is_active=True,
        role__in=['moderateur', 'membre']
    ).order_by('last_name')
    
    return render(request, 'site_web/public_member_list.html', {
        'members': members
    })

def public_member_detail(request, pk):
    """Détail d'un membre"""
    member = get_object_or_404(
        CustomUser,
        pk=pk,
        is_active=True,
        role__in=['moderateur', 'membre']
    )
    
    return render(request, 'site_web/public_member_detail.html', {
        'member': member.get_public_profile()
    })

from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

def public_guelekan_list(request):
    # Récupérer seulement les Guelekan publiés
    guelekans = Guelekan.objects.filter(status='published').order_by('-publish_at')
    
    # Pagination (10 éléments par page)
    paginator = Paginator(guelekans, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'site_web/public_guelekan_list.html', {
        'page_obj': page_obj,
    })

def public_guelekan_detail(request, slug):
    guelekan = get_object_or_404(Guelekan, slug=slug, status='published')
    return render(request, 'site_web/public_guelekan_detail.html', {
        'guelekan': guelekan,
    })