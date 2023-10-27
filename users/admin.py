from django.contrib import admin
from .models import Profile
from django.contrib import admin
from .models import User, UserProfile, Client, Attendance, Sale, Commission, RoutePlan


admin.site.register(Profile)
admin.site.register(UserProfile)
admin.site.register(Client)
admin.site.register(Attendance)
admin.site.register(Sale)
admin.site.register(Commission)
admin.site.register(RoutePlan)