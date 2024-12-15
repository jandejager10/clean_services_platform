from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from checkout.models import Order
from bookings.models import Booking
from .forms import UserProfileForm
import stripe
from django.conf import settings
from .utils import send_account_deletion_email


@login_required
def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = UserProfileForm(instance=profile)

    # Get user's orders
    orders = Order.objects.filter(user=request.user).order_by('-date')

    template = 'accounts/profile.html'
    context = {
        'form': form,
        'on_profile_page': True,
        'orders': orders,
    }

    return render(request, template, context)


@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        email = user.email  # Store email before deletion
        
        # Set Stripe API key
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        # Cancel any pending orders
        orders = Order.objects.filter(user=user, status='pending')
        for order in orders:
            # Initiate refund through Stripe
            stripe.Refund.create(payment_intent=order.stripe_pid)
            order.status = 'cancelled'
            order.save()
        
        # Cancel any pending bookings
        bookings = Booking.objects.filter(user=user, status='pending')
        for booking in bookings:
            booking.status = 'cancelled'
            booking.save()
            
        try:
            send_account_deletion_email(user)
        except Exception as e:
            print(f"Failed to send deletion email: {e}")
            
        user.delete()
        messages.success(request, 'Your account has been successfully deleted.')
        return redirect('home:index')
    
    return render(request, 'accounts/delete_account.html') 