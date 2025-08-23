from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'prenom', 'nom', 'role')
        
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
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'accept': 'image/*'})
    )

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
        user.username = user.email
        user.set_unusable_password()
        
        # Attribuer l'image uploadée
        profile_picture = self.cleaned_data.get('profile_picture')
        if profile_picture:
            user.profile_picture = profile_picture
    
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

from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

CustomUser = get_user_model()

class CustomUserUpdateForm(UserChangeForm):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=_("Le numéro doit être au format: '+999999999'. Jusqu'à 15 chiffres.")
    )
    
    phone_number = forms.CharField(
        label=_('Téléphone'),
        validators=[phone_regex],
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '+33612345678'})
    )
    
    password = None  # Nous gérons le mot de passe séparément
    
    class Meta:
        model = CustomUser
        fields = [
            'nom',
            'prenom',
            'email',
            'phone_number',
            'role',
            'is_active',
            'date_started',
            'profile_picture',
            'bio',
            'job_title',
            'department',
            'social_facebook',
            'social_linkedin',
            'social_twitter',
            'social_instagram'
        ]
        labels = {
            'is_active': _('Compte actif'),
            'date_started': _('Date de début'),
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'date_started': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personnalisation des champs
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['role'].widget.attrs.update({'class': 'form-select'})
        
        # Si l'utilisateur n'est pas admin, on restreint les champs modifiables
        if not self.instance.is_admin and not kwargs.get('initial', {}).get('is_admin', False):
            self.fields.pop('role')
            self.fields.pop('is_active')
            self.fields.pop('date_started')