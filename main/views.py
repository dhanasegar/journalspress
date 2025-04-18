from django.shortcuts import get_object_or_404, render, redirect
from .forms import PaperSubmissionForm, AuthorFormSet
from .models import Author, Journal, JournalDetail, SubmittedPaper
from django.contrib import messages

# Import JOURNAL_CHOICES from models
from .models import JOURNAL_CHOICES

from django.shortcuts import get_object_or_404, render, redirect
from .forms import PaperSubmissionForm, AuthorFormSet
from .models import Author, Journal, JournalDetail, SubmittedPaper
from django.contrib import messages

def home(request):
    # Filter by approved papers (status='approved')
    category = request.GET.get('category', None)
    papers = SubmittedPaper.objects.filter(status='approved')
    
    if category and category != 'all':
        papers = papers.filter(journal=category)
    
    context = {
        'papers': papers,
        'JOURNAL_CHOICES': JOURNAL_CHOICES,
    }
    return render(request, 'home.html', context)

def journals(request):
    """Render all approved journals with filtering"""
    category = request.GET.get('category', None)
    papers = SubmittedPaper.objects.filter(status='approved')
    
    if category and category != 'all':
        papers = papers.filter(journal=category)
    
    context = {
        'papers': papers,
        'JOURNAL_CHOICES': JOURNAL_CHOICES,
    }
    return render(request, 'journals.html', context)

# ... rest of your views remain the same ...

def about(request):
   
    return render(request, 'about.html')

def callforpapers(request):
  
    return render(request, 'callforpapers.html')

# views.py
def submit_paper(request):
    if request.method == 'POST':
        paper_form = PaperSubmissionForm(request.POST, request.FILES)
        author_formset = AuthorFormSet(request.POST, prefix='authors')
        
        if paper_form.is_valid() and author_formset.is_valid():
            paper = paper_form.save(commit=False)
            paper.status = 'submitted'
            paper.save()
            
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

# def journals(request):
#     """Render all approved journals with filtering"""
#     category = request.GET.get('category', None)
#     papers = SubmittedPaper.objects.filter(is_approved=True)
    
#     if category and category != 'all':
#         papers = papers.filter(journal=category)
    
#     context = {
#         'papers': papers,
#         'JOURNAL_CHOICES': JOURNAL_CHOICES,
#     }
#     return render(request, 'journals.html', context)

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

# views.py
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def journal_detail(request, journal_code):
    journal = get_object_or_404(Journal, code=journal_code)
    
    # Get approved papers for this specific journal
    papers = SubmittedPaper.objects.filter(
        journal=journal,
        status='approved'
    ).order_by('-approved_at')
    
    # Get or create journal details
    detail, created = JournalDetail.objects.get_or_create(journal=journal)
    
    context = {
        'journal': journal,
        'detail': detail,
        'papers': papers,
    }
    return render(request, 'journal_detail.html', context)  
@login_required
def dashboard(request):
    # For authors
    submitted_papers = SubmittedPaper.objects.filter(
        authors__email=request.user.email
    ).distinct().order_by('-submitted_at')
    
    # For admin
    if request.user.is_staff:
        pending_papers = SubmittedPaper.objects.filter(status='submitted')
        approved_papers = SubmittedPaper.objects.filter(status='approved')
    else:
        pending_papers = None
        approved_papers = None
    
    context = {
        'submitted_papers': submitted_papers,
        'pending_papers': pending_papers,
        'approved_papers': approved_papers,
    }
    return render(request, 'dashboard.html', context)
    