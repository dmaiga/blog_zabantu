from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label='Votre nom', max_length=100)
    email = forms.EmailField(label='Votre email')
    message = forms.CharField(label='Votre message', widget=forms.Textarea)