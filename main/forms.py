from django import forms
from .models import Journal, Submission, Author

JOURNAL_CHOICES = [
    ('', '-- Select Journal --'),  # Empty/default option
    ('Pharmacy', 'Pharmacy'),
    ('Management', 'Management'),
    ('Physics', 'Physics'),
    ('Applied Chemistry', 'Applied Chemistry'),
    ('Applied Mathematics', 'Applied Mathematics'),
    ('Applied Science', 'Applied Science'),
    ('Sports', 'Sports'),
    ('Physical Education', 'Physical Education'),
    ('Yoga', 'Yoga'),
    ('Physiotherapy', 'Physiotherapy'),
    ('Agriculture', 'Agriculture'),
    ('Legal Education', 'Legal Education'),
    ('Medical Research', 'Medical Research'),
    ('Clinical Research', 'Clinical Research'),
    ('Mechanical Engineering', 'Mechanical Engineering'),
    ('Electrical Engineering', 'Electrical Engineering'),
    ('Computer Engineering', 'Computer Engineering'),
    ('Software Engineering', 'Software Engineering'),
]

class PaperSubmissionForm(forms.ModelForm):
    journal = forms.ChoiceField(choices=JOURNAL_CHOICES, widget=forms.Select(attrs={'class': 'w-full p-2 border rounded'}))
    

    class Meta:
        model = Submission
        fields = ['journal', 'title', 'abstract', 'keywords', 'paper_file', 'cover_image']
        widgets = {
            'abstract': forms.Textarea(attrs={'rows': 5, 'class': 'w-full p-2 border rounded'}),
            'title': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'keywords': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'paper_file': forms.FileInput(attrs={'class': 'w-full p-2 border rounded'}),
            'cover_image': forms.FileInput(attrs={'class': 'w-full p-2 border rounded'}),
            'journal': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['journal'].queryset = Journal.objects.filter(is_published=True)
        self.fields['journal'].empty_label = "-- Select Journal --"

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'country', 'organization', 'website']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-2 border rounded'}),
            'phone_number': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'country': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'organization': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'website': forms.URLInput(attrs={'class': 'w-full p-2 border rounded'}),
        }

AuthorFormSet = forms.modelformset_factory(
    Author,
    form=AuthorForm,
    extra=1,
    can_delete=False
)