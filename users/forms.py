from django import forms
from .models import Profile, UserProfile
from django.contrib.auth.models import User


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address', 'zipcode', 'city', 'state']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['default_phone_number', 'default_street_address1', 'default_street_address2', 'default_town_or_city', 'default_county', 'default_postcode', 'default_country']
