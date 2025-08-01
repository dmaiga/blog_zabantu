from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from .models import Event
from .forms import EventForm

# Créer un événement
@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)  
        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user  
            event.save()
            return redirect('event_detail', id=event.id)
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})


# Modifier un événement
@login_required
def event_update(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event) 
        if form.is_valid():
            form.save()
            return redirect('event_detail', id=event.id)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form})


# Supprimer un événement
@login_required
def event_delete(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'events/event_delete.html', {'event': event})


# Liste des événements
@login_required
def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})


# Détail d’un événement
@login_required
def event_detail(request, id):
    event = get_object_or_404(Event, id=id)
    return render(request, 'events/event_detail.html', {'event': event})
