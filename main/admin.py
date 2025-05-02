# main/admin.py
from django.contrib import admin
from .models import Journal, JournalSubmission


admin.site.site_header = "SciManPress Admin"
admin.site.site_title = "SciManPress Portal"
admin.site.index_title = "Welcome to SciManPress Admin Dashboard"

@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_approved')
    list_filter = ('is_approved',)
    search_fields = ('name',)

@admin.register(JournalSubmission)
class JournalSubmissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'journal', 'submitted_at', 'status')
    list_filter = ('status', 'submitted_at')
    search_fields = ('title', 'first_name', 'last_name', 'email')
    actions = ['approve_submissions', 'reject_submissions']

    def approve_submissions(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, "Selected submissions have been approved.")
    approve_submissions.short_description = "Approve selected submissions"

    def reject_submissions(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, "Selected submissions have been rejected.")
    reject_submissions.short_description = "Reject selected submissions"