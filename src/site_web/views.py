from django.shortcuts import render, get_object_or_404
from articles.models import Article,Guelekan
from events.models import Event
from gallery.models import Photo,Gallery
from django.views.generic import TemplateView
from django.utils import timezone
from django.db.models import Count,Q
from django.http import Http404
from users.models import CustomUser
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.cache import cache



#09_08
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator

def public_member_detail(request, pk):
    """Détail d'un membre"""
    member = get_object_or_404(
        CustomUser,
        pk=pk,
        is_active=True,
        role__in=['moderateur', 'membre']
    )
    
    # Récupérer les articles publiés dont le membre est auteur
    articles = Article.objects.filter(
        authors=member,
        status='published'
    ).order_by('-publish_at')
    
    return render(request, 'site_web/public_member_detail.html', {
        'member': member,
        'articles': articles
    })

#09_08
#------------------------------------------------------------------------------
#06_08_2025
# views.py

from django.shortcuts import render, get_object_or_404
from users.models import CustomUser
from articles.models import Article

def membre_liste(request):
    # Récupérer tous les membres actifs
    membres = CustomUser.objects.filter(is_active=True).order_by('nom')
    
    # Préparer les données pour chaque membre
    membres_data = []
    for membre in membres:
        publications_recentes = Article.objects.filter(
            authors=membre,
            status='published'
        ).order_by('-publish_at')[:3]  # 3 publications les plus récentes
        
        membres_data.append({
            'membre': membre,
            'publications_count': Article.objects.filter(authors=membre, status='published').count(),
            'publications_recentes': publications_recentes,
        })
    
    context = {
        'membres': membres_data,
        'title': 'Notre équipe de recherche'
    }
    return render(request, 'site_web/public_membre_liste.html', context)

def membre_detail(request, user_id):
    membre = get_object_or_404(CustomUser, id=user_id, is_active=True)
    
    # Récupérer toutes les publications publiées du membre
    publications = Article.objects.filter(
        authors=membre,
        status='published'
    ).order_by('-publish_at')
    
    context = {
        'membre': membre,
        'publications': publications,
        'title': f'Profil de {membre.prenom} {membre.nom}'
    }
    return render(request, 'site_web/public_membre_detail.html', context)


# site_web/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm

def contact(request):
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Enregistre dans la BD
            messages.success(request, "Merci ! Votre message a été enregistré ✅")
            return redirect('contact')  # recharge la page
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = ContactForm()
    
      # Coordonnées pour la carte
    map_embed_url = "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3859.227623693815!2d-7.987846684716715!3d12.672381921394377!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMTLCsDQwJzIwLjYiTiA3wrA1OScxNS4xIlc!5e1!3m2!1sfr!2sfr!4v1620000000000!5m2!1sfr!2sfr"

    context = {
        'form': form,  # ton formulaire
        'map_embed_url': map_embed_url,
        'page_title': "Contact - Zabantu",
        'social_links': {
            'linkedin': "https://www.linkedin.com/company/zabantu-ecs/about/",
            'facebook': "https://www.facebook.com/zabantu.ecs",
            'twitter': "#",
            'researchgate': "#"
        }
    }
    return render(request, 'site_web/public_contact.html', context)
def liste_galeries(request):
    """Affiche la liste des galeries (version publique)"""
    galeries_list = Gallery.objects.all().order_by('-created_at')
    paginator = Paginator(galeries_list, 12)
    
    page_number = request.GET.get('page')
    galeries = paginator.get_page(page_number)
    
    return render(request, 'site_web/public_liste_galeries.html', {
        'galeries': galeries,
        'page_title': "Galerie Photos du Blog"
    })

def detail_galerie(request, slug):
    """Affiche une galerie spécifique avec ses photos"""
    galerie = get_object_or_404(Gallery, slug=slug)
    photos = galerie.photos.all().order_by('-uploaded_at')
    
    paginator = Paginator(photos, 24)
    page_number = request.GET.get('page')
    photos_page = paginator.get_page(page_number)
    
    return render(request, 'site_web/public_detail_galerie.html', {
        'galerie': galerie,
        'photos': photos_page,
        'page_title': f"Galerie : {galerie.title}"
    })

def toutes_photos(request):
    """Affiche toutes les photos du site"""
    photos_list = Photo.objects.all().order_by('-uploaded_at')
    paginator = Paginator(photos_list, 36)
    
    page_number = request.GET.get('page')
    photos = paginator.get_page(page_number)
    
    return render(request, 'site_web/public_toutes_photos.html', {
        'photos': photos,
        'page_title': "Toutes les photos du blog"
    })

def detail_photo(request, pk):
    """Affiche le détail d'une photo spécifique"""
    photo = get_object_or_404(Photo, pk=pk)
    return render(request, 'site_web/public_detail_photo.html', {
        'photo': photo,
        'page_title': f"Photo : {photo.title}"
    })
#06_08_2025
#------------------------------------------------------------------------------
#Start with public gallery 
#Contact
#membres
#------------------------------------------------------------------------------
#05_08_2025

from django.contrib.auth import get_user_model
import random

User = get_user_model()

def about_view(request):
    # Récupérer tous les membres actifs
    active_members = list(User.objects.filter(
        is_active=True,
        role__in=['moderateur', 'membre']
    ))
    
    # Sélectionner 4 membres aléatoires si on en a assez
    if len(active_members) > 4:
        active_members = random.sample(active_members, 4)
    else:
        # Si moins de 4 membres, prendre tous les membres disponibles
        active_members = active_members[:4]
    
    context = {
        'active_members': active_members,
    }
    return render(request, 'site_web/public_about.html', context)


#05_08
#______________________________________________________________________________
CATEGORY_LABELS = {
    'article': 'Articles & Publications Académiques',  
    'analyse': 'Analyses',
    'policy': 'Policy Briefs',
    'ouvrage': 'Ouvrages',
    'rapport': 'Rapports'
}

def public_article_list(request):
    current_filter = request.GET.get('type')
    search_query = request.GET.get('q')
    sort_option = request.GET.get('sort', 'date_desc')
    
    articles = Article.objects.filter(status='published')
    
    # Filtrage spécial pour les articles (inclut scholar)
    if current_filter == 'article':
        articles = articles.filter(Q(category='article') | Q(category='scholar'))
    elif current_filter:  # Filtrage normal pour les autres catégories
        articles = articles.filter(category=current_filter)
    
    # Recherche
    if search_query:
        articles = articles.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query) |
            Q(subtitle__icontains=search_query)
        )
    
    # Tri
    if sort_option == 'date_asc':
        articles = articles.order_by('created_at')
    elif sort_option == 'title_asc':
        articles = articles.order_by('title')
    elif sort_option == 'title_desc':
        articles = articles.order_by('-title')
    else:  # date_desc par défaut
        articles = articles.order_by('-created_at')
    
    # Compteurs pour les filtres (modifié pour inclure scholar dans 'article')
    total_count = Article.objects.filter(status='published').count()
    guelekan_count = Guelekan.objects.filter(status='published').count()
    
    category_counts_qs = Article.objects.filter(status='published') \
        .values('category') \
        .annotate(count=Count('id'))
    
    # Calcul spécial pour le regroupement article/scholar
    category_counts = {}
    for item in category_counts_qs:
        if item['category'] == 'scholar':
            category_counts['article'] = category_counts.get('article', 0) + item['count']
        else:
            category_counts[item['category']] = item['count']
    
    category_data = [
        (key, CATEGORY_LABELS[key], category_counts.get(key, 0))
        for key in CATEGORY_LABELS
    ]
    
    # Pagination
    paginator = Paginator(articles, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'articles': page_obj,
        'current_filter': current_filter,
        'category_data': category_data,
        'total_count': total_count,
        'guelekan_count': guelekan_count,
        'is_paginated': paginator.num_pages > 1,
    }
    return render(request, 'site_web/public_article_list.html', context)


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
    
    # Récupérer les participants organisateurs
    organizers = {
        'moderators': event.moderators.all(),
        'speakers': event.speakers.all(),
        'trainers': event.trainers.all(),
    }
    
    # Vérifier si l'événement est passé
    is_past_event = event.date < timezone.now()
    
    # Événements similaires (même type)
    similar_events = Event.objects.filter(
        is_published=True,
        event_type=event.event_type
    ).exclude(pk=event.pk).order_by('-date')[:3]
    
    return render(request, 'site_web/public_event_detail.html', {
        'event': event,
        'is_past_event': is_past_event,
        'organizers': organizers,
        'similar_events': similar_events,
    })

def public_member_list(request):
    """Liste des membres publics"""
    members = CustomUser.objects.filter(
        is_active=True,
        role__in=['moderateur', 'membre']
    ).order_by('last_name')
    
    return render(request, 'site_web/public_member_list.html', {
        'members': members
    })

class HomeView(TemplateView):
    template_name = 'site_web/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Derniers articles publiés - version optimisée
        context['latest_articles'] = Article.objects.filter(
            status='published',
           
        ).order_by('-created_at')[:4]
        
        # Événements à venir
        context['upcoming_events'] = Event.objects.filter(
            is_published=True,
            date__gte=timezone.now()
        ).order_by('date')[:3]
        
        # Mise en avant spéciale - version optimisée
        context['featured_seminar'] = Guelekan.objects.filter(
            status='published',
           
        ).order_by('-created_at').first()
        
        return context


from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator
from articles.models import Guelekan

def public_guelekan_list(request):
    guelekans = Guelekan.objects.filter(
        status='published',
        
    ).order_by('-publish_at')
    
    paginator = Paginator(guelekans, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'site_web/public_guelekan_list.html', {
        'page_obj': page_obj,
        'timezone': timezone
    })

from django.db.models import Count

def public_guelekan_detail(request, slug):
    guelekan = get_object_or_404(
        Guelekan, 
        slug=slug, 
        status='published',
    )
    
    
    galleries = guelekan.galleries.all().prefetch_related('photos').annotate(
        annotated_photo_count=Count("photos")  
    )
    
    context = {
        'guelekan': guelekan,
        'galleries': galleries,
    }
    
    return render(request, 'site_web/public_guelekan_detail.html', context)


from django.shortcuts import redirect
from django.contrib import messages
from .forms import NewsletterForm
from .models import NewsletterSubscriber

def newsletter_subscribe(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if not NewsletterSubscriber.objects.filter(email=email).exists():
                form.save()
                messages.success(request, " Vous avez été ajouté à la newsletter avec succès.")
            else:
                messages.info(request, " Vous êtes déjà inscrit à la newsletter.")
        else:
            messages.error(request, " Veuillez entrer un email valide.")
    # Toujours rediriger vers la page d’où vient le formulaire
    return redirect(request.META.get('HTTP_REFERER', 'index'))
