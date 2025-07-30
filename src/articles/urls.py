from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.article_list, name='article_list'),
    path('article/nouveau/', views.article_create, name='article_create'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('article/<slug:slug>/edit/', views.article_update, name='article_update'),
    path('media-library/', views.media_library, name='media_library'),
    path('article/<slug:slug>/publish/', views.publish_article, name='publish_article'),
    path('article/<slug:slug>/unpublish/', views.unpublish_article, name='unpublish_article'),
]
