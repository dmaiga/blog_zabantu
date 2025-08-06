from django.contrib import admin
from .models import Event,ExternalParticipant

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'is_published')
    list_filter = ('is_published', 'date')
    search_fields = ('title', 'content')

@admin.register(ExternalParticipant)
class ExternalParticipantAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'participant_type', 'organization')
    list_filter = ('participant_type',)
    search_fields = ('first_name', 'last_name', 'organization')