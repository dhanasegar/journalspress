from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Journal

def home(request):
    journals = JournalSubmission.objects.filter(status='approved')
    categories = [
        "Pharmacy", "Management", "Physics", "Applied Chemistry", "Applied Mathematics",
        "Applied Science", "Sports", "Physical Education", "Yoga", "Physiotherapy",
        "Agriculture", "Legal Education", "Medical Research", "Clinical Research",
        "Mechanical Engineering", "Electrical Engineering", "Computer Engineering",
        "Software Engineering"
    ]
    selected_category = request.GET.get('category', '')
    if selected_category:
        journals = journals.filter(journal__name=selected_category)
    return render(request, 'home.html', {'journals': journals, 'categories': categories, 'selected_category': selected_category})

def about(request):
    return render(request, 'about.html')

def callforpapers(request):
    return render(request, 'callforpapers.html')





def conference(request):
    return render(request, 'conference.html')
# main/views.py
# main/views.py
from django.shortcuts import render, redirect
from .models import Journal, JournalSubmission
from django.contrib import messages
import os
from django.conf import settings

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
            'phone': request.POST.get('phone'),
            'country': request.POST.get('country'),
            'organization': request.POST.get('organization'),
            'website': request.POST.get('website'),
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
        
        journal_submission = JournalSubmission(
            journal_id=form1_data['journal'],
            title=form1_data['title'],
            abstract=form1_data['abstract'],
            keywords=form1_data['keywords'],
            cover_image=os.path.relpath(form1_data['cover_path'], settings.MEDIA_ROOT),
            first_name=form1_data['first_name'],
            last_name=form1_data['last_name'],
            email=form1_data['email'],
            phone=form1_data['phone'],
            country=form1_data['country'],
            organization=form1_data['organization'],
            website=form1_data['website'],
            about=form2_data['about'],
            aim_scope=form2_data['aim_scope'],
            call_for_papers=form2_data['call_for_papers'],
            author_guidelines=form2_data['author_guidelines'],
            editorial_board=form2_data['editorial_board'],
            archive=form2_data['archive'],
            indexes=form2_data['indexes'],
            downloads=form2_data['downloads']
        )
        journal_submission.save()
        
        del request.session['form1_data']
        messages.success(request, 'Paper submitted successfully!')
        return redirect('journal_list')
    return redirect('submit_paper')

# main/views.py (update journal_list only)
def journal_list(request):
    journals = JournalSubmission.objects.filter(status='approved')
    categories = [
        "Pharmacy", "Management", "Physics", "Applied Chemistry", "Applied Mathematics",
        "Applied Science", "Sports", "Physical Education", "Yoga", "Physiotherapy",
        "Agriculture", "Legal Education", "Medical Research", "Clinical Research",
        "Mechanical Engineering", "Electrical Engineering", "Computer Engineering",
        "Software Engineering"
    ]
    selected_category = request.GET.get('category', '')
    if selected_category:
        journals = journals.filter(journal__name=selected_category)
    return render(request, 'journals.html', {'journals': journals, 'categories': categories, 'selected_category': selected_category})

def journal_details(request, journal_id):
    journal = JournalSubmission.objects.get(id=journal_id)
    return render(request, 'partials/journal_detail.html', {'journal': journal})

def admin_approve(request, journal_id):
    if request.user.is_staff:
        journal = JournalSubmission.objects.get(id=journal_id)
        journal.status = 'approved'  # Updated to use status
        journal.save()
        messages.success(request, 'Journal approved successfully!')
    return redirect('admin:index')

# Add this to your views.py
from django.contrib.auth.decorators import login_required

@login_required
def dash(request):
    # Get user's submitted papers
    submitted_papers = JournalSubmission.objects.filter(email=request.user.email)
    
    # Admin-specific data
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
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ConferenceSubmissionForm
from .models import ConferenceSubmission

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




    