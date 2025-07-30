from django.urls import path
from .views import public_article_list, public_article_detail

urlpatterns = [
    path('blog/', public_article_list, name='public_article_list'),
    path('blog/<slug:slug>/', public_article_detail, name='public_article_detail'),
]
