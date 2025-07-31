from django.views.generic import ListView, DetailView
from .models import Event

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    queryset = Event.objects.filter(is_published=True).order_by('-date')

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'