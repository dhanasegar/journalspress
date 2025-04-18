from django.db import models
from django.utils import timezone

# Constants (moved to top for better organization)
JOURNAL_CHOICES = [
    ('PHARM', 'Pharmacy'),
    ('MGMT', 'Management'),
    ('PHYS', 'Physics'),
    ('CHEM', 'Applied Chemistry'),
    ('MATH', 'Applied Mathematics'),
    ('SCI', 'Applied Science'),
    ('SPORT', 'Sports'),
    ('PE', 'Physical Education'),
    ('YOGA', 'Yoga'),
    ('PHYSIO', 'Physiotherapy'),
    ('AGRI', 'Agriculture'),
    ('LAW', 'Legal Education'),
    ('MED', 'Medical Research'),
    ('CLIN', 'Clinical Research'),
    ('MECH', 'Mechanical Engineering'),
    ('EEE', 'Electrical Engineering'),
    ('CSE', 'Computer Engineering'),
]

COUNTRY_CHOICES = [
    ('IN', 'India'),
    ('US', 'United States'),
    ('UK', 'United Kingdom'),
]

class Journal(models.Model):
    """Main journal model representing each unique journal"""
    code = models.CharField(
        max_length=100,
        choices=JOURNAL_CHOICES,
        primary_key=True
    )
    title = models.CharField(max_length=200)
    issn = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='journal_covers/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_journal_display(self):
        return dict(JOURNAL_CHOICES).get(self.code, self.code)

class JournalDetail(models.Model):
    """Detailed information about each journal"""
    journal = models.OneToOneField(
        Journal,
        on_delete=models.CASCADE,
        related_name='details',
       
    )
    id = models.AutoField(primary_key=True)
    about = models.TextField(blank=True, default='About this journal...')
    aim_scope = models.TextField(blank=True, default='Journal aims and scope...')
    call_for_papers = models.TextField(blank=True, default='Call for papers information...')
    author_guidelines = models.TextField(blank=True, default='Author submission guidelines...')
    editorial_board = models.TextField(blank=True, default='Editorial board members...')
    indexes = models.TextField(blank=True, default='Indexing information...')
    contact_info = models.TextField(blank=True, default='Contact details...')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Journal Detail'
        verbose_name_plural = 'Journal Details'
    
    def __str__(self):
        return f"Details for {self.journal.title}"

class SubmittedPaper(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    journal = models.ForeignKey(
        Journal,
        on_delete=models.PROTECT,
        related_name='submitted_papers'
    )
    title = models.CharField(max_length=200)
    abstract = models.TextField()
    keywords = models.CharField(max_length=200)
    upload = models.FileField(upload_to='papers/%Y/%m/%d/')
    cover_image = models.ImageField(upload_to='paper_covers/%Y/%m/%d/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Submitted Paper'
        verbose_name_plural = 'Submitted Papers'
    
    @property
    def is_approved(self):
        return self.status == 'approved'

class Author(models.Model):
    """Authors of submitted papers"""
    paper = models.ForeignKey(
        SubmittedPaper,
        on_delete=models.CASCADE,
        related_name='authors'
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    country = models.CharField(max_length=100, choices=COUNTRY_CHOICES)
    organization = models.CharField(max_length=200)
    website = models.URLField(blank=True)
    is_corresponding = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return f"{self.full_name} ({self.organization})"