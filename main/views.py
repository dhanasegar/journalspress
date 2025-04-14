from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from .forms import PaperSubmissionForm, AuthorForm

def home(request):
    """Render the home page"""
    return render(request, 'home.html')

def about(request):
    """Render the about page"""
    return render(request, 'about.html')

def callforpapers(request):
    """Render the call for papers page"""
    return render(request, 'callforpapers.html')


def submit_paper(request):
    """
    Handle paper submission with multiple authors.
    Requires user to be logged in.
    """
    AuthorFormSet = formset_factory(AuthorForm, extra=1)
    
    if request.method == 'POST':
        paper_form = PaperSubmissionForm(request.POST, request.FILES)
        author_formset = AuthorFormSet(request.POST, prefix='authors')
        
        if paper_form.is_valid() and author_formset.is_valid():
            # Save the paper submission
            submission = paper_form.save(commit=False)
            submission.submitted_by = request.user
            submission.save()
            
            # Save all authors
            authors = []
            for author_form in author_formset:
                author = author_form.save()
                authors.append(author)
                if author_form.cleaned_data.get('corresponding'):
                    submission.corresponding_author = author
                    submission.save()
            
            # Add authors to submission
            submission.authors.set(authors)
            
            return redirect('submission_success')
    else:
        paper_form = PaperSubmissionForm()
        author_formset = AuthorFormSet(prefix='authors')
    
    context = {
        'paper_form': paper_form,
        'author_formset': author_formset
    }
    return render(request, 'submitpaper.html', context)

def submission_success(request):
    """Render the submission success page"""
    return render(request, 'submission_success.html')