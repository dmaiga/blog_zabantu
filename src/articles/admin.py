
from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'list_authors', 'category', 'status', 'created_at']
    search_fields = ['title', 'authors__username']
    list_filter = ['status', 'category', 'created_at']

    def list_authors(self, obj):
        return ", ".join([author.get_full_name() or author.username for author in obj.authors.all()])
    list_authors.short_description = "Auteurs"
