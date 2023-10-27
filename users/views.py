from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required, permission_required
import time
import datetime
from .models import Attendance, Client, Commission, Sale
from .forms import AttendanceForm, ClientForm, LoginForm, RegisterForm, SaleForm, UpdateProfileForm, UpdateUserForm 
import calendar
from django.db.models import Sum, F, Case, When, Value, IntegerField
from django.db.models.functions import Coalesce
from django.db.models.functions import TruncMonth


@login_required
def home(request):
    return render(request, 'users/home.html')


# @login_required
# @permission_required('your_app.add_sale', raise_exception=True)
def add_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sales')
    else:
        form = SaleForm()
    return render(request, 'users/add_sale.html', {'form': form})

def display_sales(request):
    sales = Sale.objects.all()
    return render(request, 'users/display_sales.html', {'sales': sales})

def monthly_sales(request):
    monthly_totals = Sale.objects.annotate(
        month=TruncMonth('date_paid')
    ).values('month').annotate(total_amount_paid=Sum('loan_amount_paid')).order_by('month')

    return render(request, 'users/monthly_sales.html', {'monthly_totals': monthly_totals})

# def calculate_commission(amount_paid):
#     if 0 <= amount_paid <= 19000:
#         return 0
#     elif 20000 <= amount_paid <= 100000:
#         return 1500
#     elif 101000 <= amount_paid <= 200000:
#         return 4000
#     elif 201000 <= amount_paid <= 250000:
#         return 10000
#     elif 251000 <= amount_paid <= 550000:
#         return 12000
#     elif 551000 <= amount_paid <= 850000:
#         return 15000
#     else:
#         return 20000

def monthly_sales(request):
    monthly_totals = Sale.objects.annotate(
        month=TruncMonth('date_paid')
    ).values('month').annotate(total_amount_paid=Sum('loan_amount_paid')).order_by('month')

    # Define allowances for different ranges of total amount paid
    allowances = {
        (0, 19000): 0,
        (20000, 100000): 1500,
        (101000, 200000): 4000,
        (201000, 250000): 10000,
        (251000, 550000): 12000,
        (551000, 850000): 15000,
    }

    # Calculate and update the commission for each sale
    for entry in monthly_totals:
        total_amount_paid = entry['total_amount_paid']
        for amount_range, allowance in allowances.items():
            if amount_range[0] <= total_amount_paid <= amount_range[1]:
                commission = (total_amount_paid * Decimal('0.05')) + Decimal(allowance)
                entry['commission'] = commission

    return render(request, 'users/monthly_sales.html', {'monthly_totals': monthly_totals})


# @login_required
def managementView(request):
    return render(request, 'users/management.html')

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)
        return reverse_lazy('home')


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def add_client(request):
    total_clients = Client.objects.count()  # Get the count of clients
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.user = request.user
            client.save()
            return redirect('success_page')
    else:
        form = ClientForm()

    return render(request, 'users/add_client.html', {'form': form, 'total_clients': total_clients})


def calendar_view(request):
    # Create a calendar object
    cal = calendar.HTMLCalendar(calendar.SUNDAY)

    # Generate the HTML for the current month's calendar
    html_calendar = cal.formatmonth(2023, 10)

    # You can customize the year and month as needed
    # Replace 2023 and 10 with the desired year and month values

    return render(request, 'users/record_attendance.html', {'calendar': html_calendar})

@login_required
def record_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            user = request.user
            date = datetime.date.today()
            latitude = form.cleaned_data['latitude']
            longitude = form.cleaned_data['longitude']
            timestamp = datetime.datetime.now()

            try:
                Attendance.objects.create(user=user, date=date, location=f"({latitude}, {longitude})", latitude=latitude, longitude=longitude, timestamp=timestamp)
                # Display a JavaScript alert
                return render(request, 'users/record_attendance.html', {'form': form, 'success_message': 'Attendance recorded successfully!'})
            except Exception as e:
                error_message = f"Error occurred: {str(e)}"
                return render(request, 'users/record_attendance.html', {'form': form, 'error_message': error_message})
    else:
        form = AttendanceForm()

    return render(request, 'users/record_attendance.html', {'form': form})

def success_view(request):
    return render(request, 'users/success.html')

@login_required
def user_clients(request):
    # Display clients added by the currently logged-in user
    clients = Client.objects.filter(user=request.user)
    return render(request, 'users/user_clients.html', {'clients': clients})

def client_details(request, pk):
    client = get_object_or_404(Client, pk=pk)
    return render(request, 'users/client_details.html', {'client': client})

def attendance_success(request):
    return render(request, 'attendance_success.html')

def charts(request):
    return render(request, 'users/chats.html')

def commission_page(request):
    # Retrieve the agent's commission and sales data
    agent = request.user
    commission = Commission.objects.get(agent=agent)
    sales = Sale.objects.filter(agent=agent)

    return render(request, 'users/commission_page.html', {'commission': commission, 'sales': sales})