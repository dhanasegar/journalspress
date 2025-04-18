# Generated by Django 5.2 on 2025-04-18 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_submittedpaper_abstract_alter_submittedpaper_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submittedpaper',
            name='is_approved',
        ),
        migrations.AddField(
            model_name='submittedpaper',
            name='approved_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='submittedpaper',
            name='status',
            field=models.CharField(choices=[('submitted', 'Submitted'), ('under_review', 'Under Review'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='submitted', max_length=20),
        ),
        migrations.AlterField(
            model_name='submittedpaper',
            name='abstract',
            field=models.TextField(),
        ),
    ]
