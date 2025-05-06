from django.db import models
from django.core.validators import FileExtensionValidator

class Journal(models.Model):
    name = models.CharField(max_length=200)
    is_approved = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)  # Added to match form reference
    
    def __str__(self):
        return self.name

class JournalSubmission(models.Model):
    STATUS_CHOICES = (
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    abstract = models.TextField()
    keywords = models.CharField(max_length=500)
    cover_image = models.ImageField(upload_to='covers/')
    # paper_file = models.FileField(upload_to='papers/')  # Added missing field
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)  # Standardized to phone_number
    country = models.CharField(max_length=100)
    organization = models.CharField(max_length=200)
    website = models.URLField(blank=True)
    about = models.TextField(blank=True)
    aim_scope = models.TextField(blank=True)
    call_for_papers = models.TextField(blank=True)
    author_guidelines = models.TextField(blank=True)
    editorial_board = models.TextField(blank=True)
    archive = models.TextField(blank=True)
    indexes = models.TextField(blank=True)
    downloads = models.FileField(upload_to='downloads/', blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='under_review')

    def __str__(self):
        return self.title

class ConferenceSubmission(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    conference_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    brochure = models.FileField(
        upload_to='conference_brochures/',
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])],
        blank=True,
        null=True
    )
    
    submitter_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.conference_name} - {self.submitter_name}"