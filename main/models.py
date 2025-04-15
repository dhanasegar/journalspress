from django.db import models

JOURNAL_CHOICES = [
    ('AI', 'Artificial Intelligence'),
    ('DS', 'Data Science'),
    ('SE', 'Software Engineering'),
    ('BIO', 'Bioinformatics'),
]

COUNTRY_CHOICES = [
    ('IN', 'India'),
    ('US', 'United States'),
    ('UK', 'United Kingdom'),
]

class SubmittedPaper(models.Model):
    journal = models.CharField(max_length=100, choices=JOURNAL_CHOICES)
    keywords = models.CharField(max_length=200)
    upload = models.FileField(upload_to='papers/')
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_journal_display()} - {self.keywords}"

class Author(models.Model):
    paper = models.ForeignKey(SubmittedPaper, on_delete=models.CASCADE, related_name='authors')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    country = models.CharField(max_length=100, choices=COUNTRY_CHOICES)
    organization = models.CharField(max_length=200)
    website = models.URLField(blank=True)
    is_corresponding = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"