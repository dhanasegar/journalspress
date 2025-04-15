# models.py

from django.db import models

JOURNAL_CHOICES = [
    ('AI', 'Artificial Intelligence'),
    ('DS', 'Data Science'),
    ('SE', 'Software Engineering'),
    ('BIO', 'Bioinformatics'),
    # Add more as needed
]

class SubmittedPaper(models.Model):
    journal = models.CharField(max_length=100, choices=JOURNAL_CHOICES)
    author_info = models.TextField()
    keywords = models.CharField(max_length=200)
    upload = models.FileField(upload_to='uploads/')
    is_approved = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.journal} - {self.keywords}"
