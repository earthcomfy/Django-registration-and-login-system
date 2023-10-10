
from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', home, name='users-home'),
    # path('home/', views.home_view, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('add_client/', views.add_client, name='add_client'),
    path('success/', views.success_page, name='success_page'), 
    
    path('calendar/', views.calendar_view, name='calendar_view'),
    path('attendance/', views.record_attendance, name='record_attendance'),
    
    

  
]
