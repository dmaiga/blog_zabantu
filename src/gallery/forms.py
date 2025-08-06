from django import forms
from .models import Gallery, Photo

class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['title', 'description', 'cover_image', 'is_featured']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'caption', 'image', 'gallery', 'is_standalone']
        widgets = {
            'caption': forms.Textarea(attrs={'rows': 3}),
            'gallery': forms.Select(attrs={'class': 'form-control'}),
        }