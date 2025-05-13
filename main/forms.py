from django import forms
from .models import Journal, JournalSubmission, ConferenceSubmission

JOURNAL_CHOICES = [
    ('', '-- Select Journal --'),
    ('Pharmacy', 'Pharmacy'),
    # ... keep your other choices ...
]

class PaperSubmissionForm(forms.ModelForm):
    class Meta:
        model = JournalSubmission
        fields = [
            'journal', 'title', 'abstract', 'keywords', 'cover_image', 'first_name',
            'last_name', 'email', 'phone_number',
            'country', 'organization', 'website'
        ]
        widgets = {
            'abstract': forms.Textarea(attrs={'rows': 5, 'class': 'w-full p-2 border rounded'}),
            'title': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'keywords': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            # 'paper_file': forms.FileInput(attrs={'class': 'w-full p-2 border rounded'}),
            'cover_image': forms.FileInput(attrs={'class': 'w-full p-2 border rounded'}),
            'journal': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'first_name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-2 border rounded'}),
            'phone_number': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'country': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'organization': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'website': forms.URLInput(attrs={'class': 'w-full p-2 border rounded'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['journal'].queryset = Journal.objects.filter(is_published=True)
        self.fields['journal'].empty_label = "-- Select Journal --"

# Removed AuthorForm and AuthorFormSet as they're not needed with the combined form

class ConferenceSubmissionForm(forms.ModelForm):
    class Meta:
        model = ConferenceSubmission
        fields = [
            'conference_name', 'location', 'start_date', 'end_date', 'brochure',
            'submitter_name', 'phone_number', 'email'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={
        'type': 'date', 
        'class': 'w-full p-3 rounded-lg bg-purple-50 text-purple-900 border border-purple-200 focus:ring-4 focus:ring-purple-300 focus:border-purple-500 transition-all'
    }),
    'end_date': forms.DateInput(attrs={
        'type': 'date', 
        'class': 'w-full p-3 rounded-lg bg-purple-50 text-purple-900 border border-purple-200 focus:ring-4 focus:ring-purple-300 focus:border-purple-500 transition-all'
    }),
    'conference_name': forms.TextInput(attrs={
        'class': 'w-full p-3 rounded-lg bg-purple-50 text-purple-900 border border-purple-200 focus:ring-4 focus:ring-purple-300 focus:border-purple-500 transition-all'
    }),
    'location': forms.TextInput(attrs={
        'class': 'w-full p-3 rounded-lg bg-purple-50 text-purple-900 border border-purple-200 focus:ring-4 focus:ring-purple-300 focus:border-purple-500 transition-all'
    }),
    'brochure': forms.FileInput(attrs={
        'class': 'w-full p-3 rounded-lg bg-purple-50 text-purple-900 border border-purple-200 focus:ring-4 focus:ring-purple-300 focus:border-purple-500 transition-all file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-purple-600 file:text-white hover:file:bg-purple-700 transition-all'
    }),
    'submitter_name': forms.TextInput(attrs={
        'class': 'w-full p-3 rounded-lg bg-purple-50 text-purple-900 border border-purple-200 focus:ring-4 focus:ring-purple-300 focus:border-purple-500 transition-all'
    }),
    'phone_number': forms.TextInput(attrs={
        'class': 'w-full p-3 rounded-lg bg-purple-50 text-purple-900 border border-purple-200 focus:ring-4 focus:ring-purple-300 focus:border-purple-500 transition-all'
    }),
    'email': forms.EmailInput(attrs={
        'class': 'w-full p-3 rounded-lg bg-purple-50 text-purple-900 border border-purple-200 focus:ring-4 focus:ring-purple-300 focus:border-purple-500 transition-all'
    }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("End date must be after start date.")
        
        return cleaned_data