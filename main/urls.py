from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('callforpapers/', views.callforpapers, name='callforpapers'),
    path('submitpaper/', views.submit_paper, name='submit_paper'),
    path('journals/', views.journals, name='journals')

]