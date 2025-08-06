from django import forms
from django.utils import timezone
from .models import Event, ExternalParticipant

class EventForm(forms.ModelForm):
    moderators = forms.ModelMultipleChoiceField(
        queryset=ExternalParticipant.objects.filter(participant_type='moderator'),
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        required=False,
        label="Modérateurs externes"
    )
    
    speakers = forms.ModelMultipleChoiceField(
        queryset=ExternalParticipant.objects.filter(participant_type='speaker'),
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        required=False,
        label="Intervenants externes"
    )
    
    trainers = forms.ModelMultipleChoiceField(
        queryset=ExternalParticipant.objects.filter(participant_type='trainer'),
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        required=False,
        label="Formateurs externes"
    )
    
    class Meta:
        model = Event
        fields = [
            'title', 'event_type', 'content', 'image', 
            'date', 'end_date', 'location', 'lieu_gps',
            'is_published', 'moderators', 'speakers', 'trainers'
        ]
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'content': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'event_type': "Type d'événement",
            'lieu_gps': "Lien Google Maps"
        }
    
    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        end_date = cleaned_data.get('end_date')
        
        if date and date < timezone.now():
            raise forms.ValidationError("La date de l'événement ne peut pas être dans le passé")
        
        if end_date and date and end_date < date:
            raise forms.ValidationError("La date de fin ne peut pas être avant la date de début")
        
        return cleaned_data

class ExternalParticipantForm(forms.ModelForm):
    class Meta:
        model = ExternalParticipant
        fields = '__all__'
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'first_name': "Prénom",
            'last_name': "Nom",
            'participant_type': "Rôle"
        }