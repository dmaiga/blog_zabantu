from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'role')
        
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomMemberCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'email', 'nom', 'prenom',
            'phone_number', 'profile_picture',
            'bio', 'job_title', 'department', 'date_started',
            'social_facebook', 'social_linkedin', 'social_twitter',
        ]
        widgets = {
            'date_started': forms.DateInput(attrs={'type': 'date'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'membre'
        user.username = user.email  # email devient username
        user.set_unusable_password()
        if commit:
            user.save()
        return user

from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.core.validators import RegexValidator
from .models import CustomUser

class ProfileEditForm(forms.ModelForm):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Le numéro doit être au format: '+999999999'. Jusqu'à 15 chiffres."
    )
    
    phone_number = forms.CharField(
        validators=[phone_regex],
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': '+261 34 12 345 67'
        })
    )
    
    class Meta:
        model = CustomUser
        fields = [
            'profile_picture',
            'nom',
            'prenom',
            'email',
            'phone_number',
            'job_title',
            'department',
            'bio',
            'social_facebook',
            'social_linkedin',
            'social_twitter',
            'social_instagram'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})