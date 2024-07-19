from django.contrib import admin
from .models import UserProfile, Transaction

admin.site.register(UserProfile)
admin.site.register(Transaction)