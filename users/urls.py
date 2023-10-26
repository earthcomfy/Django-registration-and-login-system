
from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', home, name='users-home'),
    path('managements/', views.managementView, name='management_page'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('add_client/', views.add_client, name='add_client'),
    path('success/', views.success_view, name='success_page'),
    path('success/', views.attendance_success, name='attendance_success'),  
    
    path('calendar/', views.calendar_view, name='calendar_view'),
    path('attendance/', views.record_attendance, name='record_attendance'),
    
    path('user-clients/', views.user_clients, name='user_clients'),
    # path('admin-clients/', views.admin_clients, name='admin_clients'),
    path('client/<int:pk>/', views.client_details, name='client_details'),
    path('charts/', views.charts, name='charts_page'),

    # path('add_sales/', views.enter_client_data, name='enter_client_data'),
    # path('agent-page/<int:agent_id>/', views.agent_page, name='agent_page'),
    # path('add-sale/', views.add_sale, name='add_sale'),
    path('commission/', views.commission_page, name='commission_page'),
    
    path('add_sale/', views.add_sale, name='add_sale'),
    path('sales/', views.display_sales, name='sales'),
    path('monthly_sales/', views.monthly_sales, name='monthly_sales'),
    # path('monthly_commissions/', views.monthly_commissions, name='monthly_commissions'),
]
