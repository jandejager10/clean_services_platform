from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Profile

# Create your views here.
@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'users/profile.html', context)

@login_required
def update_profile(request):
  if request.method == 'POST':
    form = ProfileForm(request.POST, instance=request.user.profile)
    if form.is_valid():
      form.save()
      return redirect('profile_success_url') # Redirect after successful update
  else:
    form = ProfileForm(instance=request.user.profile)
  return render(request, 'update_profile.html', {'form': form})