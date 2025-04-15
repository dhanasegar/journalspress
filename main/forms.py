# forms.py
from django import forms
from .models import SubmittedPaper

class PaperSubmissionForm(forms.ModelForm):
    class Meta:
        model = SubmittedPaper
        fields = ['journal', 'author_info', 'keywords', 'upload']
        widgets = {
            'journal': forms.Select(attrs={'class': 'block w-full p-2 border rounded-md'}),
            'author_info': forms.Textarea(attrs={'class': 'block w-full p-2 border rounded-md', 'rows': 3}),
            'keywords': forms.TextInput(attrs={'class': 'block w-full p-2 border rounded-md'}),
            'upload': forms.ClearableFileInput(attrs={'class': 'block w-full'}),
        }
