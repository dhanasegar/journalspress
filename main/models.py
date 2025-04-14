from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

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

class Journal(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=JOURNAL_CATEGORIES)
    description = models.TextField()
    issn = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    organization = models.CharField(max_length=200)
    website = models.URLField(blank=True, null=True)
    corresponding = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Submission(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('revisions_required', 'Revisions Required'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('published', 'Published'),
    ]
    
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    abstract = models.TextField()
    keywords = models.TextField(help_text="One keyword per line")
    paper_file = models.FileField(upload_to='submissions/')
    authors = models.ManyToManyField(Author)
    corresponding_author = models.ForeignKey(
        Author, 
        on_delete=models.SET_NULL,
        null=True,
        related_name='corresponding_submissions'
    )
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    submission_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='submitted'
    )
    revision_notes = models.TextField(blank=True, null=True)
    published_date = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Set published date when status changes to published
        if self.status == 'published' and not self.published_date:
            self.published_date = timezone.now()
        super().save(*args, **kwargs)