from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Profile, RoutePlan, UserProfile
from .models import Client, Sale


class RegisterForm(UserCreationForm):
    # fields we want to include and customize in our form
    first_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name',
                                                               'class': 'form-control',
                                                               }))
    last_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name',
                                                              'class': 'form-control',
                                                              }))
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control',
                                                           }))
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()
        # Generate the agent code
        user_profile = UserProfile(user=user, agent_code=f'COACL{UserProfile.objects.count() + 1:03d}')
        user_profile.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                 'class': 'form-control',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name': 'password',
                                                                 }))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.fields['pf_number'].widget.attrs['disabled'] = True
        self.fields['amount'].widget.attrs['disabled'] = True
        self.fields['comment'].widget.attrs['disabled'] = True
        self.fields['pf_number_conversion'].widget.attrs['disabled'] = True
        self.fields['password'].widget.attrs['disabled'] = True
        self.fields['amount_applied'].widget.attrs['disabled'] = True
        self.fields['date_field'].widget.attrs['disabled'] = True
        self.fields['type_loan_qualify'].widget.attrs['disabled'] = True
        self.fields['comment_conversion'].widget.attrs['disabled'] = True
        
class AttendanceForm(forms.Form):
    latitude = forms.CharField(widget=forms.HiddenInput())
    longitude = forms.CharField(widget=forms.HiddenInput())
    
class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['agent', 'client_name', 'loan_amount_paid', 'date_paid']
        
        
class RoutePlanForm(forms.ModelForm):
    agent = forms.ModelChoiceField(queryset=User.objects.all().order_by('username'))

    class Meta:
        model = RoutePlan
        fields = ['date', 'agent', 'institution', 'location']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'agent': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 40%;'}),
            'institution': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 40%;'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 40%;'}),
        }