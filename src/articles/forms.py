# articles/forms.py
from django import forms
from tinymce.widgets import TinyMCE
from .models import Article
from users.models import CustomUser

#09_08


#________________________________________________________________
class ArticleForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCE(
            attrs={
                'cols':50, 
                'rows': 5,
                'plugins': 'preview autolink visualblocks image media table help',
                'toolbar': 'undo redo | styles | bold italic | alignleft aligncenter alignright | bullist numlist outdent indent | link image | preview media | help',
            }
        ),
        required=False,
        label="Contenu",
        help_text="Utilisez l'éditeur pour formater votre contenu (facultatif)"
    )
    
    is_academic = forms.BooleanField(
        required=False,
        label="Publication académique",
        help_text="Cocher si c'est une publication académique"
    )

    class Meta:
        model = Article
        fields = [
            'title', 'subtitle', 'category', 'authors', 'cover_image', 'content',
            'pdf_file', 'status', 'is_academic', 'publisher', 'journal', 
            'publication_date', 'abstract', 'scholar_link'
        ]
        widgets = {
            'authors': forms.SelectMultiple(attrs={'class': 'select2'}),
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
            'abstract': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Entrez un résumé concis...'}),
            'subtitle': forms.TextInput(attrs={'placeholder': 'Sous-titre facultatif...'}),
        }
        labels = {
            'publisher': "Éditeur (facultatif)",
            'journal': "Revue (facultatif)",
            'publication_date': "Date de publication",
            'abstract': "Résumé",
            'scholar_link': "Lien Scholar (facultatif)",
            'cover_image': "Image de couverture (facultative)",
        }
        help_texts = {
            'publisher': "Nom de l'éditeur ou de la maison d'édition",
            'journal': "Nom de la revue ou du journal académique",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Initialisation pour les instances existantes
        if self.instance.pk:
            self.fields['is_academic'].initial = self.instance.category == 'scholar'
        
        # Configuration dynamique des champs
        self.setup_field_requirements()
        
        # Tous les utilisateurs peuvent voir tous les autres utilisateurs comme auteurs potentiels
        self.fields['authors'].queryset = CustomUser.objects.all()
        
        # Options de statut
        self.fields['status'].choices = [
            ('draft', 'Brouillon'),
            ('published', 'Publié'),
        ]
        self.fields['status'].initial = 'draft'

        # Rendre certains champs non obligatoires
        self.fields['subtitle'].required = False
        self.fields['cover_image'].required = False
        self.fields['publisher'].required = False
        self.fields['journal'].required = False

    def setup_field_requirements(self):
        """Configure dynamiquement les champs requis en fonction du type d'article"""
        is_academic = self.data.get('is_academic') if self.data else self.initial.get('is_academic', False)
        
        if is_academic:
            self.fields['content'].required = False
            self.fields['abstract'].required = True
            self.fields['publication_date'].required = True
            self.fields['category'].initial = 'scholar'
            self.fields['category'].widget = forms.HiddenInput()
        else:
            self.fields['content'].required = True
            self.fields['abstract'].required = False
            self.fields['publication_date'].required = False

    def clean(self):
        cleaned_data = super().clean()
        is_academic = cleaned_data.get('is_academic')
        
        # Suppression de la validation obligatoire pour l'image de couverture
        # if cleaned_data.get('status') == 'published' and not cleaned_data.get('cover_image'):
        #     raise forms.ValidationError("Une image de couverture est requise pour la publication")
        
        if is_academic:
            if not cleaned_data.get('publication_date'):
                raise forms.ValidationError("La date de publication est obligatoire pour les publications académiques")
            cleaned_data['category'] = 'scholar'
        
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data.get('is_academic'):
            instance.category = 'scholar'
        if commit:
            instance.save()
            self.save_m2m()
        return instance



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