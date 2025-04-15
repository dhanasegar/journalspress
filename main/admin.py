# journals view
from .models import SubmittedPaper

def journals(request):
    published = SubmittedPaper.objects.filter(is_approved=True)
    return render(request, 'journals.html', {'papers': published})
# admin.py
from django.contrib import admin
from .models import SubmittedPaper

admin.site.register(SubmittedPaper)
