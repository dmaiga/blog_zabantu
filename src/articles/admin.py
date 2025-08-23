
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


from django.contrib import admin
from .models import Guelekan

@admin.register(Guelekan)
class GuelekanAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'created_at', 'publish_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'subtitle', 'content']
    filter_horizontal = ['galleries'] 
    
    # Masquer complètement les champs meta et slug de l'interface admin
    # Ils seront générés automatiquement
    exclude = ['meta_title', 'meta_description', 'slug']
    
    # Champs à afficher dans l'admin (seulement ceux que vous voulez que l'utilisateur remplisse)
    fieldsets = (
        ('Contenu principal', {
            'fields': ('title', 'subtitle', 'content', 'status')
        }),
        ('Intervenants', {
            'fields': ('guests',),
            'description': 'Entrez un intervenant par ligne'
        }),
        ('Médias', {
            'fields': ('cover_image', 'pdf_file', 'galleries')
        }),
        ('Publication', {
            'fields': ('publish_at',),
            'classes': ('collapse',),
            'description': 'Optionnel: planifiez la publication'
        })
    )