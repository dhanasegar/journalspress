# main/models.py
from django.db import models

class Journal(models.Model):
    name = models.CharField(max_length=200)
    is_approved = models.BooleanField(default=False)
    
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
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    organization = models.CharField(max_length=200)
    website = models.URLField()
    about = models.TextField()
    aim_scope = models.TextField()
    call_for_papers = models.TextField()
    author_guidelines = models.TextField()
    editorial_board = models.TextField()
    archive = models.TextField()
    indexes = models.TextField()
    downloads = models.FileField(upload_to='downloads/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='under_review')  # Replaced approved

    def __str__(self):
        return self.title