
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

# articles/admin.py
from django.contrib import admin
from .models import Guelekan

@admin.register(Guelekan)
class GuelekanAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'created_at', 'publish_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'subtitle', 'content']
    filter_horizontal = ['galleries'] 
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Contenu', {
            'fields': ('title', 'subtitle', 'content', 'status')
        }),
        ('Médias', {
            'fields': ('cover_image', 'pdf_file', 'galleries')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Dates', {
            'fields': ('publish_at',),
            'classes': ('collapse',)
        })
    )