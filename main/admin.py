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

    from django.contrib import admin
from .models import ConferenceSubmission
from django.utils.html import format_html
from django.urls import reverse
from django.http import HttpResponseRedirect

@admin.register(ConferenceSubmission)
class ConferenceSubmissionAdmin(admin.ModelAdmin):
    list_display = (
        'conference_name',
        'location',
        'date_range',
        'submitter_name',
        'email',
        'status',
        'created_at',
        'admin_actions',
    )
    list_filter = ('status', 'start_date', 'created_at')
    search_fields = ('conference_name', 'location', 'submitter_name', 'email')
    readonly_fields = ('created_at', 'updated_at', 'brochure_preview')
    fieldsets = (
        ('Conference Details', {
            'fields': (
                'conference_name',
                'location',
                'start_date',
                'end_date',
                'brochure',
                'brochure_preview',
            )
        }),
        ('Submitter Information', {
            'fields': (
                'submitter_name',
                'phone_number',
                'email',
            )
        }),
        ('Administration', {
            'fields': (
                'status',
                'admin_notes',
                'created_at',
                'updated_at',
            )
        }),
    )
    actions = ['approve_selected', 'reject_selected']
    list_per_page = 20

    def date_range(self, obj):
        return f"{obj.start_date} to {obj.end_date}"
    date_range.short_description = 'Date Range'

    def brochure_preview(self, obj):
        if obj.brochure:
            return format_html(
                '<a href="{}" target="_blank">Download Brochure</a>',
                obj.brochure.url
            )
        return "No brochure uploaded"
    brochure_preview.short_description = 'Brochure'

    def admin_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">Approve</a>&nbsp;'
            '<a class="button" href="{}">Reject</a>',
            reverse('admin:conference_approve', args=[obj.pk]),
            reverse('admin:conference_reject', args=[obj.pk]),
        )
    admin_actions.short_description = 'Actions'

    def approve_selected(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f'{updated} conference(s) approved.')
    approve_selected.short_description = "Approve selected conferences"

    def reject_selected(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} conference(s) rejected.')
    reject_selected.short_description = "Reject selected conferences"

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:pk>/approve/',
                self.admin_site.admin_view(self.approve_conference),
                name='conference_approve',
            ),
            path(
                '<int:pk>/reject/',
                self.admin_site.admin_view(self.reject_conference),
                name='conference_reject',
            ),
        ]
        return custom_urls + urls

    def approve_conference(self, request, pk):
        conference = ConferenceSubmission.objects.get(pk=pk)
        conference.status = 'approved'
        conference.save()
        self.message_user(request, 'Conference approved successfully.')
        return HttpResponseRedirect(reverse('admin:main_conferencesubmission_changelist'))

    def reject_conference(self, request, pk):
        conference = ConferenceSubmission.objects.get(pk=pk)
        conference.status = 'rejected'
        conference.save()
        self.message_user(request, 'Conference rejected.')
        return HttpResponseRedirect(reverse('admin:main_conferencesubmission_changelist'))