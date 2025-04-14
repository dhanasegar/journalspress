from django import forms
from .models import Journal, Author, Submission
import os

JOURNAL_CATEGORIES = [
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

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = [
            'first_name', 'last_name', 'email', 'phone_number',
            'country', 'organization', 'website', 'corresponding'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Country'
            }),
            'organization': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Organization/Institution'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Website (optional)'
            }),
            'corresponding': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'corresponding': 'Corresponding Author'
        }

class PaperSubmissionForm(forms.ModelForm):
    journal = forms.ModelChoiceField(
        queryset=Journal.objects.filter(is_active=True),
        empty_label="-- Select Journal --",
        widget=forms.Select(attrs={
            'class': 'form-select',
            'required': 'required'
        })
    )
    
    keywords = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Enter one keyword per line'
        }),
        help_text="Enter one keyword per line"
    )
    
    paper_file = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.doc,.docx'
        }),
        help_text="Accepted formats: PDF, DOC, DOCX (Max 10MB)"
    )

    class Meta:
        model = Submission
        fields = ['journal', 'title', 'abstract', 'keywords', 'paper_file']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Paper Title'
            }),
            'abstract': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Enter your abstract here...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # You can add custom initialization here if needed
    
    def clean_paper_file(self):
        paper_file = self.cleaned_data.get('paper_file')
        if paper_file:
            valid_extensions = ['.pdf', '.doc', '.docx']
            extension = os.path.splitext(paper_file.name)[1].lower()
            if extension not in valid_extensions:
                raise forms.ValidationError(
                    'Unsupported file format. Please upload a PDF or Word document.'
                )
            if paper_file.size > 10 * 1024 * 1024:  # 10MB
                raise forms.ValidationError(
                    'File size exceeds the 10MB limit.'
                )
        return paper_file

# Optional: Formset for multiple authors
AuthorFormSet = forms.formset_factory(
    AuthorForm,
    extra=1,
    can_delete=False,
    can_order=False
)