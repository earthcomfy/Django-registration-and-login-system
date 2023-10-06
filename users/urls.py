from django.urls import path
from .views import home, profile, RegisterView,add_client

urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('add_client/', views.add_client, name='add_client'),
]
