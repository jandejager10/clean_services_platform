from django.db import models
from django import forms

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from allauth.account.signals import user_signed_up
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.base import ProviderAccount



# Create your models here.
User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.user.username} - Profile"

# This is a custom signal handler to create a user profile upon user signup
def create_profile(sender, **kwargs):
    user = kwargs['user']
    if not Profile.objects.filter(user=user).exists():
        Profile.objects.create(user=user)

user_signed_up.connect(create_profile)

class ProfileForm(forms.ModelForm):
  class Meta:
    model = Profile
    exclude = ['user'] # exclude user field as it's a one-to-one relationship with the User model