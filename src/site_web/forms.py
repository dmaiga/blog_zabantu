from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label='Votre nom', max_length=100)
    email = forms.EmailField(label='Votre email')
    message = forms.CharField(label='Votre message', widget=forms.Textarea)


from django import forms
from .models import NewsletterSubscriber

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Votre email',
                'required': True,
            })
        }

# users/forms.py ou site_web/forms.py

from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Votre email'}),
            'subject': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('collaboration', 'Collaboration'),
                ('information', 'Demande d\'information'),
                ('other', 'Autre')
            ]),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Votre message'}),
        }
