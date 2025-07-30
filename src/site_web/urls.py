from django.urls import path
from .views import article_list_public, article_detail_public

urlpatterns = [
    path('blog/', article_list_public, name='public_article_list'),
    path('blog/<slug:slug>/', article_detail_public, name='public_article_detail'),
]
