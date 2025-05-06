from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.conf import settings
from django.urls import reverse
import os

from .models import Journal, JournalSubmission, ConferenceSubmission
from .forms import ConferenceSubmissionForm


# Main pages views
def home(request):
    journals = JournalSubmission.objects.filter(status='approved')
    categories = Journal.objects.filter(
        is_approved=True, 
        is_published=True
    ).values_list('name', flat=True).distinct()
    
    # Debug print (remove after testing)
    print("Categories from database:", list(categories))
    
    selected_category = request.GET.get('category', '')
    if selected_category:
        journals = journals.filter(journal__name=selected_category)
    
    return render(request, 'home.html', {
        'journals': journals,
        'categories': categories,
        'selected_category': selected_category
    })

def about(request):
    return render(request, 'about.html')

def callforpapers(request):
    return render(request, 'callforpapers.html')

def conference(request):
    return render(request, 'conference.html')


# Journal submission views
def submit_paper(request):
    journals = Journal.objects.all()
    return render(request, 'submit_paper.html', {'journals': journals})

def submit_paper2(request):
    if request.method == 'POST':
        form_data = {
            'journal': request.POST.get('journal'),
            'title': request.POST.get('title'),
            'abstract': request.POST.get('abstract'),
            'keywords': request.POST.get('keywords'),
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone', ''),  # Make phone optional
            'country': request.POST.get('country'),
            'organization': request.POST.get('organization'),
            'website': request.POST.get('website', ''),  # Make website optional
        }
        
        cover_image = request.FILES.get('cover_image')
        if cover_image:
            cover_path = os.path.join(settings.MEDIA_ROOT, 'covers', cover_image.name)
            os.makedirs(os.path.dirname(cover_path), exist_ok=True)
            with open(cover_path, 'wb+') as destination:
                for chunk in cover_image.chunks():
                    destination.write(chunk)
            form_data['cover_path'] = cover_path
            
            request.session['form1_data'] = form_data
            return render(request, 'submit_paper2.html', {'form_data': form_data})
        else:
            messages.error(request, "Please upload a cover image.")
            return redirect('submit_paper')
    return redirect('submit_paper')

def submit_complete(request):
    if request.method == 'POST':
        form1_data = request.session.get('form1_data', {})
        form2_data = request.POST.copy()
        form2_data.update(request.FILES)
        
        try:
            journal_submission = JournalSubmission(
                journal_id=form1_data.get('journal'),
                title=form1_data.get('title'),
                abstract=form1_data.get('abstract'),
                keywords=form1_data.get('keywords'),
                first_name=form1_data.get('first_name'),
                last_name=form1_data.get('last_name'),
                email=form1_data.get('email'),
                phone_number=form1_data.get('phone', ''),  # Default empty string
                country=form1_data.get('country'),
                organization=form1_data.get('organization'),
                website=form1_data.get('website', ''),  # Default empty string
                about=form2_data.get('about', ''),
                aim_scope=form2_data.get('aim_scope', ''),
                call_for_papers=form2_data.get('call_for_papers', ''),
                author_guidelines=form2_data.get('author_guidelines', ''),
                editorial_board=form2_data.get('editorial_board', ''),
                archive=form2_data.get('archive', ''),
                indexes=form2_data.get('indexes', ''),
                downloads=form2_data.get('downloads', '')
            )
            
            if 'cover_path' in form1_data:
                journal_submission.cover_image = os.path.relpath(form1_data['cover_path'], settings.MEDIA_ROOT)
            
            journal_submission.save()
            
            del request.session['form1_data']
            messages.success(request, 'Paper submitted successfully!')
            return redirect('journal_list')
            
        except Exception as e:
            messages.error(request, f'Error submitting paper: {str(e)}')
            return redirect('submit_paper')
    
    return redirect('submit_paper')


# Journal listing and details views
def journal_list(request):
    journals = JournalSubmission.objects.filter(status='approved')
    # Get distinct journal names for categories
    categories = Journal.objects.filter(
        is_approved=True, 
        is_published=True
    ).values_list('name', flat=True).distinct()
    
    selected_category = request.GET.get('category', '')
    if selected_category:
        journals = journals.filter(journal__name=selected_category)
    
    return render(request, 'journals.html', {
        'journals': journals,
        'categories': categories,
        'selected_category': selected_category
    })

def journal_details(request, journal_id):
    journal = JournalSubmission.objects.get(id=journal_id)
    return render(request, 'partials/journal_detail.html', {'journal': journal})

@login_required
def admin_approve(request, journal_id):
    if request.user.is_staff:
        journal = JournalSubmission.objects.get(id=journal_id)
        journal.status = 'approved'
        journal.save()
        messages.success(request, 'Journal approved successfully!')
    return redirect('admin:index')


# Dashboard view
@login_required
def dash(request):
    submitted_papers = JournalSubmission.objects.filter(email=request.user.email)
    
    pending_papers = None
    approved_papers = None
    
    if request.user.is_staff:
        pending_papers = JournalSubmission.objects.filter(status='under_review')
        approved_papers = JournalSubmission.objects.filter(status='approved')
    
    context = {
        'submitted_papers': submitted_papers,
        'pending_papers': pending_papers,
        'approved_papers': approved_papers,
    }
    return render(request, 'dashboard.html', context)


# Conference views
def conference_page(request):
    if request.method == 'POST':
        form = ConferenceSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your conference submission has been received and is pending approval.')
            return redirect('conference_page')
    else:
        form = ConferenceSubmissionForm()
    
    approved_conferences = ConferenceSubmission.objects.filter(status='approved').order_by('-created_at')
    
    return render(request, 'conference.html', {
        'form': form,
        'conferences': approved_conferences,
    })


# Authentication views
def register_view(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect('home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! You are now logged in.")
            next_url = request.POST.get('next') or 'home'
            return redirect(next_url)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = UserCreationForm()
    
    next_url = request.GET.get('next', '')
    
    return render(request, 'login/register.html', {
        'form': form,
        'next': next_url
    })

def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                next_url = request.POST.get('next') or 'home'
                return redirect(next_url)
        else:
            if 'username' in form.errors:
                messages.error(request, "Invalid username or password.")
            else:
                for error in form.errors.get('__all__', []):
                    messages.error(request, error)
    else:
        form = AuthenticationForm()
    
    next_url = request.GET.get('next', '')
    
    return render(request, 'login/login.html', {
        'form': form,
        'next': next_url
    })

def logout_view(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You were not logged in.")
        return redirect('home')
        
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('home')