from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.validators import RegexValidator




class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    agent_code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.agent_code
    
# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)




class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)   # Add a ForeignKey field to User
    client_fullname = models.CharField(max_length=255)
    id_number = models.CharField(
                max_length=8,  # Allow up to 8 characters
                unique=True,
                validators=[
                    RegexValidator(
                        regex=r'^[0-9]{7,8}$',  # Only digits, 7 to 8 characters
                        message='ID number must be 7 to 8 digits long.',
                    ),
                ]
            )

    phone_number = models.CharField(
                max_length=12,  # Allow up to 12 characters
                validators=[
                    RegexValidator(
                        regex=r'^[0-9]{10,12}$',  # Only digits, 10 to 12 characters
                        message='Phone number must be 10 to 12 digits long.',
                    ),
                ]
            )
    ministry = models.CharField(max_length=255)
    TYPE_CHOICES = (
        ('prospects', 'Prospects'),
        ('lead', 'Lead'),
        ('conversion', 'Conversion'),
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    pf_number = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    pf_number_conversion = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    amount_applied = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date_field = models.DateField(blank=True, null=True)
    comment_conversion = models.TextField(blank=True, null=True)
    TYPE_LOAN_CHOICES = (
        ('refinance', 'Refinance'),
        ('topup', 'Top-Up'),
        ('buyoff', 'Buy-Off'),
    )
    type_loan_qualify = models.CharField(max_length=20, choices=TYPE_LOAN_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.client_fullname


class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    location = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)  # Store latitude as a DecimalField
    longitude = models.DecimalField(max_digits=9, decimal_places=6)  # Store longitude as a DecimalField

    class Meta:
        unique_together = ('user', 'date',)
        
        
class Sale(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100)
    loan_amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateField()
    commission = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Add commission field

    def __str__(self):
        return self.client_name

class Commission(models.Model):
    agent = models.OneToOneField(User, on_delete=models.CASCADE)
    commission_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.agent.username
    
class RoutePlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    agent = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.date} - {self.agent} - {self.institution} - {self.location}"