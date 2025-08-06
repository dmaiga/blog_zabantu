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





def contact(request):
    # Liste des partenaires institutionnels
    partners = [
        {
            'name': "Université de Ségou",
            'logo': "users/images/partenaires/iufp_segou.png",
            'url': "#"  # Remplacez par l'URL réelle
        },
        {
            'name': "Université de Ghana",
            'logo': "users/images/partenaires/ghana.svg",
            'url': "#"
        },
        {
            'name': "Université Alassane Ouattara de Bouaké",
            'logo': "users/images/partenaires/uni_ao.webp",
            'url': "#"
        },
        {
            'name': "Université de Mons",
            'logo': "users/images/partenaires/uni_mons.svg",
            'url': "#"
        },
        {
            'name': "Université Libre de Bruxelles",
            'logo': "users/images/partenaires/ulb.svg",
            'url': "#"
        },
        {
            'name': "Association pour la Promotion du Numérique en Afrique",
            'logo': "users/images/partenaires/apna_logo.png",
            'url': "#"
        }
    ]

    # Coordonnées de contact
    contact_info = {
        'institution': "Campus universitaire de Badalabougou",
        'address': "BP 1234 Bamako, Mali",
        'phone': "+223 77 94 14 70",
        'email': "info@zabantu.net",
        'opening_hours': {
            'weekdays': "Lundi - Vendredi : 8h - 17h",
            'saturday': "Samedi : 9h - 13h"
        }
    }

    # Traitement du formulaire
    #if request.method == 'POST':
    #    name = request.POST.get('name')
    #    email = request.POST.get('email')
    #    subject = request.POST.get('subject')
    #    message = request.POST.get('message')
#
#   #    # Validation basique
#   #    if not all([name, email, subject, message]):
#   #        messages.error(request, "Veuillez remplir tous les champs obligatoires.")
    #    else:
    #        # Construction du sujet du mail
    #        subject_map = {
    #            'collaboration': "Proposition de collaboration",
    #            'research': "Question de recherche",
    #            'publication': "Demande concernant une publication",
    #            'conference': "Invitation à une conférence",
    #            'media': "Demande médiatique",
    #            'other': "Demande de contact"
    #        }
    #        email_subject = f"[Contact Zabantu] {subject_map.get(subject, 'Demande')} de {name}"
#
#   #        # Construction du corps du mail
#   #        email_body = f"""
#   #        Nouveau message reçu via le formulaire de contact:
    #        
    #        Nom: {name}
    #        Email: {email}
    #        Sujet: {subject_map.get(subject, subject)}
    #        
    #        Message:
    #        {message}
    #        
    #        ---
    #        Cet email a été envoyé depuis le formulaire de contact de Zabantu.
    #        """
#
#   #        try:
#   #            # Envoi de l'email
#   #            send_mail(
    #                email_subject,
    #                email_body,
    #                settings.DEFAULT_FROM_EMAIL,
    #                [settings.CONTACT_EMAIL],  # Configurez ceci dans vos settings
    #                fail_silently=False,
    #            )
    #            
    #            # Envoi d'une copie au visiteur
    #            if settings.SEND_COPY_TO_VISITOR:
    #                send_mail(
    #                    f"Confirmation de votre message à Zabantu",
    #                    f"Nous avons bien reçu votre message et y répondrons dans les plus brefs délais.\n\nVotre message:\n{message}",
    #                    settings.DEFAULT_FROM_EMAIL,
    #                    [email],
    #                    fail_silently=True,
    #                )
    #            
    #            messages.success(request, "Votre message a été envoyé avec succès!")
    #            return redirect('contact')
    #           
    #       except Exception as e:
    #           messages.error(request, f"Une erreur s'est produite lors de l'envoi du message: {str(e)}")

    # Coordonnées pour la carte (Badalabougou, Mali)
    map_embed_url = "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3859.227623693815!2d-7.987846684716715!3d12.672381921394377!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMTLCsDQwJzIwLjYiTiA3wrA1OScxNS4xIlc!5e1!3m2!1sfr!2sfr!4v1620000000000!5m2!1sfr!2sfr"

    context = {
        'partners': partners,
        'contact_info': contact_info,
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


User = get_user_model()

def about_view(request):
    # Section Identité - Données statiques
    identity_data = {
        'name': "Groupe de recherche Zabantu",
        'subtitle': "« Économie-Guerre-État »",
        'description': "Nom inspiré d'une plante locale mandingue, Zabantu est un groupe de chercheurs en sciences sociales travaillant sur le développement économique et social. C'est de ce fait un groupe pluri et interdisciplinaire, qui est ouvert à tous les chercheurs et chercheuses du monde dans l'objectif d'avoir une recherche plus inclusive et plus ancrée.",
        'vision': "Vers une recherche ancrée dans les dynamiques économiques et sociales",
        'research_domains': [
            "Économie politique",
            "Conflits et sécurité",
            "Développement social",
            "Politiques publiques",
            "Études africaines"
        ],
        'activities': {
            'guelekan': {
                'title': "Séminaire Gɛlɛkan",
                'description': [
                    "Gɛlɛkan est une tribune scientifique de collaboration et de partage d'expérience et de connaissance.",
                    "Inspiré de la tribune de sagesse bamanan réservés aux ainés, Gɛlɛkan est un espace de communication scientifique permettant aux chercheurs de partager les résultats de leurs recherches accompli ou en cours.",
                    "Les séminaires Gɛlɛkan portent aussi sur les thématiques de formation comme la méthodologie de recherche et les astuces de publications académiques."
                ]
            }
        }
    }

    # Section Équipe - Récupération des membres actifs
    cache_key = 'active_team_members'
    active_members = cache.get(cache_key)
    
    if not active_members:
        active_members = User.objects.filter(
            is_active=True,
            role__in=['admin', 'moderateur', 'membre']
        ).exclude(
            profile_picture=''
        ).order_by('-date_started')
        
        # Mise en cache pour 1 heure
        cache.set(cache_key, active_members, 3600)

    # Section Partenaires - Liste des partenaires avec leurs logos
    partners = [
        {
            'name': "Université de Ségou",
            'logo': "users/images/partenaires/ufp_segou.png",
            'url': "#"  # Remplacez par l'URL réelle
        },
        {
            'name': "Université de Ghana",
            'logo': "users/images/partenaires/ghana.svg",
            'url': "#"
        },
        {
            'name': "Université Alassane Ouattara de Bouaké",
            'logo': "users/images/partenaires/uni_ao.webp",
            'url': "#"
        },
        {
            'name': "Université de Mons",
            'logo': "users/images/partenaires/uni_mons.svg",
            'url': "#"
        },
        {
            'name': "Université Libre de Bruxelles",
            'logo': "users/images/partenaires/ulb.svg",
            'url': "#"
        },
        {
            'name': "Association pour la Promotion du Numérique en Afrique",
            'logo': "users/images/partenaires/apna_logo.png",
            'url': "#"
        }
    ]

    context = {
        'identity_data': identity_data,
        'active_members': active_members,
        'partners': partners,
        'MEDIA_URL': settings.MEDIA_URL,
        'STATIC_URL': settings.STATIC_URL
    }

    return render(request, 'site_web/public_about.html', context)




#05_08
#______________________________________________________________________________

CATEGORY_LABELS = {
    'analyse': 'Analyses',
    'article': 'Articles',
    'policy': 'Policy Briefs',
    'ouvrage': 'Ouvrages',
    'rapport': 'Rapports'
}
def public_article_list(request):
    current_filter = request.GET.get('type')
    search_query = request.GET.get('q')
    sort_option = request.GET.get('sort', 'date_desc')
    
    articles = Article.objects.filter(status='published')
    
    # Filtrage par catégorie
    if current_filter:
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
    
    # Compteurs pour les filtres
    total_count = Article.objects.filter(status='published').count()
    guelekan_count = Guelekan.objects.filter(status='published').count()
    
    category_counts_qs = Article.objects.filter(status='published') \
        .values('category') \
        .annotate(count=Count('id'))
    category_counts = {item['category']: item['count'] for item in category_counts_qs}
    
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