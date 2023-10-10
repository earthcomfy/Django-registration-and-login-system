from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required, permission_required
import time
import datetime
from .models import Attendance
from .forms import AttendanceForm 
import calendar

from .forms import *

@login_required
def home(request):
    return render(request, 'users/home.html')


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
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.user = request.user  # Set the user field to the currently logged-in user
            client.save()
            return redirect('user_clients')  # Redirect to the user's clients page
    else:
        form = ClientForm()

    return render(request, 'users/add_client.html', {'form': form})

# def calendar_view(request):
#     return render(request, 'users/calendar.html')

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
                error_message = "An error occurred while recording attendance. Please try again."
                return render(request, 'users/record_attendance.html', {'form': form, 'error_message': error_message})

    else:
        form = AttendanceForm()

    return render(request, 'users/record_attendance.html', {'form': form})