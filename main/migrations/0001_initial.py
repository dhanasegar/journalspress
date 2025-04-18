# Generated by Django 5.2 on 2025-04-17 23:08

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('journal_type', models.CharField(choices=[('PHARM', 'Pharmacy'), ('MGMT', 'Management'), ('PHYS', 'Physics'), ('CHEM', 'Applied Chemistry'), ('MATH', 'Applied Mathematics'), ('SCI', 'Applied Science'), ('SPORT', 'Sports'), ('PE', 'Physical Education'), ('YOGA', 'Yoga'), ('PHYSIO', 'Physiotherapy'), ('AGRI', 'Agriculture'), ('LAW', 'Legal Education'), ('MED', 'Medical Research'), ('CLIN', 'Clinical Research'), ('MECH', 'Mechanical Engineering'), ('EEE', 'Electrical Engineering'), ('CSE', 'Computer Engineering')], max_length=100, unique=True, verbose_name='Journal Category')),
                ('title', models.CharField(help_text='The full title of the journal', max_length=200, unique=True)),
                ('slug', models.SlugField(blank=True, help_text='URL-friendly version of the title', max_length=200, unique=True)),
                ('description', models.TextField(help_text='Brief description of the journal')),
                ('cover_image', models.ImageField(help_text='Recommended size: 1200x630 pixels', upload_to='journal_covers/')),
                ('thumbnail', models.ImageField(blank=True, help_text='Small square image for listings', null=True, upload_to='journal_thumbnails/')),
                ('issn', models.CharField(blank=True, max_length=20, verbose_name='ISSN')),
                ('eissn', models.CharField(blank=True, max_length=20, verbose_name='eISSN')),
                ('frequency', models.CharField(blank=True, help_text='Publication frequency (e.g., Monthly, Quarterly)', max_length=50)),
                ('editor_in_chief', models.CharField(blank=True, max_length=100)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('coming_soon', 'Coming Soon')], default='active', max_length=20)),
                ('about', models.TextField(blank=True, verbose_name='About the Journal')),
                ('aim_scope', models.TextField(blank=True, verbose_name='Aim and Scope')),
                ('call_for_papers', models.TextField(blank=True, verbose_name='Call for Papers')),
                ('author_guidelines', models.TextField(blank=True, verbose_name='Author Guidelines')),
                ('reach_us', models.TextField(blank=True, verbose_name='Reach Us')),
                ('contact_email', models.EmailField(blank=True, max_length=254, verbose_name='Contact Email')),
                ('contact_phone', models.CharField(blank=True, max_length=20, verbose_name='Contact Phone')),
                ('contact_address', models.TextField(blank=True, verbose_name='Contact Address')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Journal',
                'verbose_name_plural': 'Journals',
                'ordering': ['title'],
                'indexes': [models.Index(fields=['journal_type'], name='main_journa_journal_ac59af_idx'), models.Index(fields=['status'], name='main_journa_status_59be4b_idx')],
            },
        ),
        migrations.CreateModel(
            name='EditorialMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('affiliation', models.CharField(max_length=200)),
                ('role', models.CharField(max_length=100)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='editorial_photos/')),
                ('order', models.PositiveIntegerField(default=0, help_text='Ordering priority (higher numbers come first)')),
                ('bio', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('journal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='editorial_board', to='main.journal')),
            ],
            options={
                'verbose_name': 'Editorial Member',
                'verbose_name_plural': 'Editorial Board',
                'ordering': ['-order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='JournalIndex',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('url', models.URLField(blank=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='index_logos/')),
                ('journal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='indexes', to='main.journal')),
            ],
            options={
                'verbose_name': 'Journal Index',
                'verbose_name_plural': 'Journal Indexes',
            },
        ),
        migrations.CreateModel(
            name='SubmittedPaper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Untitled Paper', max_length=200)),
                ('keywords', models.CharField(max_length=200)),
                ('abstract', models.TextField(blank=True)),
                ('upload', models.FileField(upload_to='papers/')),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='paper_covers/')),
                ('status', models.CharField(choices=[('submitted', 'Submitted'), ('under_review', 'Under Review'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('published', 'Published')], default='submitted', max_length=20)),
                ('is_approved', models.BooleanField(default=False)),
                ('submission_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('publication_date', models.DateField(blank=True, null=True)),
                ('doi', models.CharField(blank=True, max_length=100)),
                ('journal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.journal')),
            ],
            options={
                'verbose_name': 'Submitted Paper',
                'verbose_name_plural': 'Submitted Papers',
                'ordering': ['-submission_date'],
            },
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=20)),
                ('country', models.CharField(choices=[('IN', 'India'), ('US', 'United States'), ('UK', 'United Kingdom')], max_length=100)),
                ('organization', models.CharField(max_length=200)),
                ('department', models.CharField(blank=True, max_length=200)),
                ('position', models.CharField(blank=True, max_length=100)),
                ('website', models.URLField(blank=True)),
                ('orcid_id', models.CharField(blank=True, max_length=20)),
                ('is_corresponding', models.BooleanField(default=False)),
                ('order', models.PositiveIntegerField(default=0)),
                ('paper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authors', to='main.submittedpaper')),
            ],
            options={
                'verbose_name': 'Author',
                'verbose_name_plural': 'Authors',
                'ordering': ['order', 'last_name'],
            },
        ),
    ]
