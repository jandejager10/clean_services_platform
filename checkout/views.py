from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required

import stripe

from cart.cart import Cart
from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from accounts.models import UserProfile
from .utils import send_order_confirmation_email


@login_required
def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    cart = Cart(request)

    if request.method == 'POST':
        # Save the save_info preference to session
        save_info = 'save_info' in request.POST
        request.session['save_info'] = save_info
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'town_or_city': request.POST['town_or_city'],
            'county': request.POST['county'],
            'postcode': request.POST['postcode'],
        }

        order_form = OrderForm(form_data)
        if order_form.is_valid():
            # Get the payment intent ID from the form
            pid = request.POST.get('client_secret').split('_secret')[0]
            
            # Create order but don't save yet
            order = order_form.save(commit=False)
            order.stripe_pid = pid
            order.user = request.user
            order.save()

            try:
                # Confirm the payment with Stripe
                stripe.api_key = stripe_secret_key
                stripe.PaymentIntent.modify(pid, 
                    metadata={'order_id': order.order_number})
                
                # Create the order line items
                for item in cart:
                    product = Product.objects.get(id=item['product'].id)
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=item['quantity'],
                    )
                    order_line_item.save()

                # Clear the cart and redirect
                cart.clear()
                return redirect(reverse('checkout:checkout_success',
                                     args=[order.order_number]))
            except stripe.error.StripeError as e:
                messages.error(request, 
                    "Payment processing error. Please try again later.")
                order.delete()
                return redirect(reverse('cart:cart_detail'))
            except Exception as e:
                messages.error(request, 
                    "There was an error processing your order. Please try again.")
                order.delete()
                return redirect(reverse('cart:cart_detail'))
    else:
        if not cart:
            messages.error(request, "Your cart is empty")
            return redirect(reverse('products:products'))

        # Try to prefill the form with user's profile data
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.default_phone_number,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'town_or_city': profile.default_town_or_city,
                    'county': profile.default_county,
                    'postcode': profile.default_postcode,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

        current_cart = cart
        total = current_cart.get_total_price()
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key

        try:
            intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=settings.STRIPE_CURRENCY,
            )
        except stripe.error.StripeError as e:
            messages.error(request, 
                "Payment system error. Please try again later.")
            return redirect(reverse('cart:cart_detail'))

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing.')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """Handle successful checkouts"""
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        order.user_profile = profile
        order.save()

        if save_info:
            profile.default_phone_number = order.phone_number
            profile.default_street_address1 = order.street_address1
            profile.default_street_address2 = order.street_address2
            profile.default_town_or_city = order.town_or_city
            profile.default_county = order.county
            profile.default_postcode = order.postcode
            profile.save()

    # Send order confirmation email
    try:
        send_order_confirmation_email(order)
    except Exception as e:
        messages.warning(request, 
            'Order confirmation email could not be sent. '
            'Please check your order history for confirmation.')

    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'cart' in request.session:
        del request.session['cart']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context) 