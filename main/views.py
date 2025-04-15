from django.shortcuts import render, redirect
from .forms import PaperSubmissionForm,AuthorFormSet
from .models import Author, SubmittedPaper

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

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import SubmittedPaper, Author
from .forms import PaperSubmissionForm, AuthorFormSet

def submit_paper(request):
    if request.method == 'POST':
        paper_form = PaperSubmissionForm(request.POST, request.FILES)
        author_formset = AuthorFormSet(request.POST, prefix='authors')
        
        if paper_form.is_valid() and author_formset.is_valid():
            # Save the paper first
            paper = paper_form.save()
            
            # Save authors and associate with paper
            authors = author_formset.save(commit=False)
            for author in authors:
                author.paper = paper
                author.save()
            
            messages.success(request, 'Your paper has been submitted successfully!')
            return redirect('submission_success')
    else:
        paper_form = PaperSubmissionForm()
        author_formset = AuthorFormSet(queryset=Author.objects.none(), prefix='authors')
    
    return render(request, 'submitpaper.html', {
        'form': paper_form,
        'formset': author_formset,
    })

def journals(request):
    """Render all approved journals"""
    papers = SubmittedPaper.objects.filter(is_approved=True)
    return render(request, 'journals.html', {'papers': papers})
