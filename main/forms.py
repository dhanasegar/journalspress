from django import forms
from django.forms import modelformset_factory
from .models import SubmittedPaper, Author

class PaperSubmissionForm(forms.ModelForm):
    class Meta:
        model = SubmittedPaper
        fields = ['journal', 'title', 'abstract', 'keywords', 'cover_image', 'upload']
        widgets = {
            'journal': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Enter paper title'
            }),
            'abstract': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
                'rows': 5,
                'placeholder': 'Enter paper abstract (200-300 words)'
            }),
            'keywords': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Separate keywords with commas'
            }),
            'cover_image': forms.ClearableFileInput(attrs={
                'class': 'hidden'
            }),
            'upload': forms.ClearableFileInput(attrs={
                'class': 'hidden'
            }),
        }
        labels = {
            'title': 'Paper Title',
            'abstract': 'Abstract',
            'keywords': 'Keywords',
            'cover_image': 'Cover Image (Recommended)',
            'upload': 'Paper File',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['abstract'].required = True
        self.fields['keywords'].required = True
        self.fields['upload'].required = True

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
            'is_corresponding': forms.CheckboxInput(attrs={'class': 'h-5 w-5 rounded border-gray-300 text-purple-600 focus:ring-purple-500 '
            'cursor-pointer transition-all duration-200', 'style': 'box-shadow: 0 0 0 2px rgba(147, 51, 234, 0.2)',}),
        }

AuthorFormSet = modelformset_factory(
    Author,
    form=AuthorForm,
    extra=1,
    can_delete=False
)

# In forms.py
from django import forms
from .models import SubmittedPaper, Author

class SubmittedPaperForm(forms.ModelForm):
    class Meta:
        model = SubmittedPaper
        fields = ['journal', 'title', 'abstract', 'keywords', 'cover_image', 'upload']
        widgets = {
            'abstract': forms.Textarea(attrs={'rows': 5}),
        }

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'country', 'organization', 'website', 'is_corresponding']