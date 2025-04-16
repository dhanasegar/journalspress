from django import forms
from django.forms import modelformset_factory
from .models import SubmittedPaper, Author

class PaperSubmissionForm(forms.ModelForm):
    class Meta:
        model = SubmittedPaper
        fields = ['journal', 'keywords', 'cover_image', 'upload']
        widgets = {
            'journal': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'keywords': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'cover_image': forms.ClearableFileInput(attrs={'class': 'w-full'}),
            'upload': forms.ClearableFileInput(attrs={'class': 'w-full'}),
        }
        labels = {
            'cover_image': 'Cover Image (Recommended)',
            'upload': 'Paper File',
        }

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'email', 'phone_number', 
                 'country', 'organization', 'website', 'is_corresponding']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-2 border rounded'}),
            'phone_number': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'country': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'organization': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'website': forms.URLInput(attrs={'class': 'w-full p-2 border rounded'}),
            'is_corresponding': forms.CheckboxInput(attrs={'class': 'ml-2'}),
        }

AuthorFormSet = modelformset_factory(
    Author,
    form=AuthorForm,
    extra=1,
    can_delete=False
)