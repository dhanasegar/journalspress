from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('callforpapers/', views.callforpapers, name='callforpapers'),
   
    path('conference/', views.conference, name='conference'),



    path('submit/', views.submit_paper, name='submit_paper'),
    path('submit/step2/', views.submit_paper2, name='submit_paper2'),
    path('submit/complete/', views.submit_complete, name='submit_complete'),
    path('journals/', views.journal_list, name='journal_list'),
    path('journal/<int:journal_id>/', views.journal_details, name='journal_details'),
    path('admin/approve/<int:journal_id>/', views.admin_approve, name='admin_approve'),
]
