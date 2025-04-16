from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('callforpapers/', views.callforpapers, name='callforpapers'),
    path('submitpaper/', views.submit_paper, name='submit_paper'),

    path('journals/', views.journals, name='journals'),

    path('filter-journals/', views.filter_journals, name='filter_journals'),
    path('submission_success/', views.submission_success, name='submission_success'),
    path('conference/', views.conference, name='conference'),

]