from django.contrib import admin
from .models import Profile

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'city', 'state', 'zipcode']
    search_fields = ['user__username', 'phone_number', 'city']