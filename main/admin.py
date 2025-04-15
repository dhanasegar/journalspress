from django.contrib import admin
from .models import SubmittedPaper, Author

class AuthorInline(admin.TabularInline):
    model = Author
    extra = 1
    show_change_link = True

class SubmittedPaperAdmin(admin.ModelAdmin):
    list_display = ('journal', 'keywords', 'is_approved', 'submitted_at')
    list_filter = ('journal', 'is_approved')
    search_fields = ('keywords',)
    inlines = [AuthorInline]
    list_editable = ('is_approved',)
    
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if not instance.pk:  # Only for new instances
                instance.paper = form.instance
            instance.save()
        formset.save_m2m()

admin.site.register(SubmittedPaper, SubmittedPaperAdmin)
admin.site.register(Author)