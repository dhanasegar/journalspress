from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from django.urls import reverse
from .models import SubmittedPaper, Author, Journal, JournalDetail

admin.site.site_header = "SciManPress Admin"
admin.site.site_title = "SciManPress Portal"
admin.site.index_title = "Welcome to SciManPress Admin"

# Author Inline for SubmittedPaper
class AuthorInline(admin.TabularInline):
    model = Author
    extra = 1
    show_change_link = True
    fields = ('first_name', 'last_name', 'email', 'is_corresponding', 'organization', 'country')
    readonly_fields = ('created_at', 'updated_at')

# SubmittedPaper Admin
class SubmittedPaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'journal', 'status', 'submitted_at', 'approved_at', 'authors_list')
    list_filter = ('status', 'journal', 'submitted_at')
    search_fields = ('title', 'abstract', 'keywords', 'authors__first_name', 'authors__last_name')
    list_editable = ('status',)
    inlines = [AuthorInline]
    readonly_fields = ('submitted_at', 'updated_at', 'approved_at', 'journal_details_link')
    fieldsets = (
        ('Paper Information', {
            'fields': ('journal', 'title', 'abstract', 'keywords')
        }),
        ('Files', {
            'fields': ('upload', 'cover_image')
        }),
        ('Status', {
            'fields': ('status', 'submitted_at', 'updated_at', 'approved_at', 'journal_details_link')
        }),
    )
    actions = ['approve_papers', 'mark_as_under_review', 'reject_papers']

    def journal_details_link(self, obj):
        if obj.journal and hasattr(obj.journal, 'details'):
            url = reverse('admin:main_journaldetail_change', args=[obj.journal.details.id])
            return format_html('<a href="{}" class="button">Edit Journal Details</a>', url)
        return "No journal details available"
    journal_details_link.short_description = 'Journal Information'
    journal_details_link.allow_tags = True

    def authors_list(self, obj):
        return ", ".join([author.full_name for author in obj.authors.all()])
    authors_list.short_description = 'Authors'

    def approve_papers(self, request, queryset):
        updated = queryset.update(status='approved', approved_at=timezone.now())
        self.message_user(request, f"{updated} papers were approved.")
    approve_papers.short_description = "Approve selected papers"

    def mark_as_under_review(self, request, queryset):
        updated = queryset.update(status='under_review')
        self.message_user(request, f"{updated} papers marked as under review.")
    mark_as_under_review.short_description = "Mark as under review"

    def reject_papers(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f"{updated} papers were rejected.")
    reject_papers.short_description = "Reject selected papers"

    def save_model(self, request, obj, form, change):
        if 'status' in form.changed_data and obj.status == 'approved' and not obj.approved_at:
            obj.approved_at = timezone.now()
        super().save_model(request, obj, form, change)

# Journal Admin
from django.contrib import admin
from .models import SubmittedPaper, Author, Journal, JournalDetail

class JournalDetailInline(admin.StackedInline):
    model = JournalDetail
    can_delete = False
    verbose_name_plural = 'Journal Details'
    fieldsets = (
        (None, {
            'fields': (
                ('about', 'aim_scope'),
                ('call_for_papers', 'author_guidelines'),
                ('editorial_board', 'indexes'),
                ('contact_info',)
            )
        }),
    )

class JournalAdmin(admin.ModelAdmin):
    inlines = [JournalDetailInline]
    list_display = ('title', 'code', 'issn', 'has_details')
    
    def has_details(self, obj):
        return hasattr(obj, 'details')
    has_details.boolean = True

admin.site.register(Journal, JournalAdmin)
admin.site.register(JournalDetail)
admin.site.register(SubmittedPaper)
admin.site.register(Author)

