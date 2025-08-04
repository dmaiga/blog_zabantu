from django.urls import path
from .views import (
    HomeView, 
    public_article_list, 
    public_article_detail,
    public_event_list,
    public_event_detail,
    public_member_list,
    public_member_detail,
    public_guelekan_list,
    public_guelekan_detail,

)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('publications/', public_article_list, name='public_article_list'),
    path('publications/<slug:slug>/', public_article_detail, name='public_article_detail'),
    path('evenements/', public_event_list, name='public_event_list'),
    path('evenements/<int:pk>/', public_event_detail, name='public_event_detail'),
    path('membres/', public_member_list, name='public_member_list'),
    path('membres/<int:pk>/', public_member_detail, name='public_member_detail'),
    # Guelekan
    path('guelekans/', public_guelekan_list, name='public_guelekan_list'),
    path('guelekans/<slug:slug>/', public_guelekan_detail, name='public_guelekan_detail'),

]