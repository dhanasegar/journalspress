from django.contrib import admin
from django.utils.html import format_html
from .models import Journal, Author, Submission

@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'category')

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'email', 'organization')
    search_fields = ('last_name', 'first_name', 'email', 'organization')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'journal', 
        'status', 
        'submission_date', 
        'published_date',
        'view_paper_link'
    )
    list_filter = ('status', 'journal', 'submission_date')
    search_fields = ('title', 'abstract', 'keywords')
    filter_horizontal = ('authors',)
    actions = ['approve_submissions', 'reject_submissions']
    readonly_fields = ('submission_date', 'published_date')
    
    def view_paper_link(self, obj):
        if obj.paper_file:
            return format_html(
                '<a href="{}" target="_blank">View Paper</a>',
                obj.paper_file.url
            )
        return "-"
    view_paper_link.short_description = "Paper"
    
    def approve_submissions(self, request, queryset):
        queryset.update(status='published')
        self.message_user(
            request, 
            f"Successfully approved {queryset.count()} submissions"
        )
    approve_submissions.short_description = "Approve selected submissions"
    
    def reject_submissions(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(
            request, 
            f"Successfully rejected {queryset.count()} submissions"
        )
    reject_submissions.short_description = "Reject selected submissions"
    
    fieldsets = (
        ('Submission Details', {
            'fields': (
                'journal', 
                'title', 
                'abstract', 
                'keywords',
                'paper_file',
                'view_paper_link'
            )
        }),
        ('Authorship', {
            'fields': ('authors', 'corresponding_author', 'submitted_by')
        }),
        ('Status', {
            'fields': (
                'status', 
                'submission_date', 
                'published_date',
                'revision_notes'
            )
        }),
    )