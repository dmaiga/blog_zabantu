# articles/forms.py
from django import forms
from tinymce.widgets import TinyMCE
from .models import Article
from users.models import CustomUser

class ArticleForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCE(
            attrs={
                'cols': 80, 
                'rows': 10,
                'plugins': 'preview autolink visualblocks image media table help',
                'toolbar': 'undo redo | styles | bold italic | alignleft aligncenter alignright | bullist numlist outdent indent | link image | preview media | help',
            }
        ),
        help_text="Utilisez l'éditeur pour formater votre contenu"
    )
    
    publish_at = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Planifier la publication",
        help_text="Laissez vide pour publier immédiatement"
    )
    
    class Meta:
        model = Article
        fields = [
            'title', 'subtitle', 'category', 'authors', 'cover_image', 'content', 
            'pdf_file', 'status', 'publish_at',
        ]
        widgets = {
            'authors': forms.SelectMultiple(attrs={'class': 'select2'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Tous les utilisateurs peuvent voir tous les autres utilisateurs comme auteurs potentiels
        self.fields['authors'].queryset = CustomUser.objects.all()
        
        self.fields['status'].choices = [
            ('draft', 'Brouillon'),
            ('published', 'Publié'),
        ]
        self.fields['status'].initial = 'draft'
    
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('status') == 'published' and not cleaned_data.get('cover_image'):
            raise forms.ValidationError("Une image de couverture est requise pour la publication")
        return cleaned_data
    

from django import forms
from tinymce.widgets import TinyMCE
from .models import Guelekan

class GuelekanForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCE(
            attrs={
                'cols': 80, 
                'rows': 10,
                'plugins': 'preview autolink visualblocks image media table help',
                'toolbar': 'undo redo | styles | bold italic | alignleft aligncenter alignright | bullist numlist outdent indent | link image | preview media | help',
            }
        ),
        help_text="Utilisez l'éditeur pour formater votre contenu"
    )
    
    publish_at = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Planifier la publication",
        help_text="Laissez vide pour publier immédiatement"
    )
    
    class Meta:
        model = Guelekan
        fields = [
            'title', 'subtitle', 'cover_image', 'content', 
            'pdf_file', 'status', 'publish_at', 'meta_title', 'meta_description'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].choices = [
            ('draft', 'Brouillon'),
            ('published', 'Publié'),
        ]
        self.fields['status'].initial = 'draft'
    
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('status') == 'published' and not cleaned_data.get('cover_image'):
            raise forms.ValidationError("Une image de couverture est requise pour la publication")
        return cleaned_data