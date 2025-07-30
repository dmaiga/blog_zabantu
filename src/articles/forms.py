# articles/forms.py
from django import forms
from tinymce.widgets import TinyMCE
from .models import Article

class ArticleForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCE(
            attrs={
                'cols': 80, 
                'rows': 30,
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
            'title', 'category', 'cover_image', 'content', 
            'pdf_file', 'status', 'publish_at',
            
        ]
        