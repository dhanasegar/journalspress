from django.shortcuts import render, redirect
from .forms import PaperSubmissionForm
from .models import SubmittedPaper

def home(request):
    """Render the home page with approved/published journals"""
    papers = SubmittedPaper.objects.filter(is_approved=True)
    return render(request, 'home.html', {'papers': papers})

def about(request):
    """Render the about page"""
    return render(request, 'about.html')

def callforpapers(request):
    """Render the call for papers page"""
    return render(request, 'callforpapers.html')

def submit_paper(request):
    """Handle paper submission form"""
    if request.method == 'POST':
        form = PaperSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # 🔥 Saves to DB
            return redirect('journals')  # Redirect to journals page
    else:
        form = PaperSubmissionForm()
    return render(request, 'submitpaper.html', {'form': form})

def journals(request):
    """Render all approved journals"""
    papers = SubmittedPaper.objects.filter(is_approved=True)
    return render(request, 'journals.html', {'papers': papers})
