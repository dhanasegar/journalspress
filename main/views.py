from django.shortcuts import render, redirect
from .forms import PaperSubmissionForm, AuthorFormSet
from .models import Author, SubmittedPaper
from django.contrib import messages

# Import JOURNAL_CHOICES from models
from .models import JOURNAL_CHOICES

def home(request):
   
    category = request.GET.get('category', None)
    papers = SubmittedPaper.objects.filter(is_approved=True)
    
    if category and category != 'all':
        papers = papers.filter(journal=category)
    
    context = {
        'papers': papers,
        'JOURNAL_CHOICES': JOURNAL_CHOICES,
    }
    return render(request, 'home.html', context)

def about(request):
   
    return render(request, 'about.html')

def callforpapers(request):
  
    return render(request, 'callforpapers.html')

def submit_paper(request):
    if request.method == 'POST':
        paper_form = PaperSubmissionForm(request.POST, request.FILES)
        author_formset = AuthorFormSet(request.POST, prefix='authors')
        
        if paper_form.is_valid() and author_formset.is_valid():
            # Save the paper first
            paper = paper_form.save(commit=False)
            paper.is_approved = False  # New submissions are not approved by default
            paper.save()
            
            # Save authors and associate with paper
            authors = author_formset.save(commit=False)
            for author in authors:
                author.paper = paper
                author.save()
            
            messages.success(request, 'Your paper has been submitted successfully! It will be published after approval.')
            return redirect('submission_success')
    else:
        paper_form = PaperSubmissionForm()
        author_formset = AuthorFormSet(queryset=Author.objects.none(), prefix='authors')
    
    return render(request, 'submitpaper.html', {
        'form': paper_form,
        'formset': author_formset,
    })

def journals(request):
    """Render all approved journals with filtering"""
    category = request.GET.get('category', None)
    papers = SubmittedPaper.objects.filter(is_approved=True)
    
    if category and category != 'all':
        papers = papers.filter(journal=category)
    
    context = {
        'papers': papers,
        'JOURNAL_CHOICES': JOURNAL_CHOICES,
    }
    return render(request, 'journals.html', context)

from django.http import JsonResponse
from django.template.loader import render_to_string

def filter_journals(request):
    category = request.GET.get('category', None)
    papers = SubmittedPaper.objects.filter(is_approved=True)
    
    if category and category != 'all':
        papers = papers.filter(journal=category)
    
    html = render_to_string('partials/journal_list.html', {
        'papers': papers,
        'request': request  # Pass request if needed for other template tags
    })
    return JsonResponse({'html': html})

def submission_success(request):
  
    return render(request, 'submission_success.html')

def conference(request):
  
    return render(request, 'conference.html')