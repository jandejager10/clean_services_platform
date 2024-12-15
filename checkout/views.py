from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

import stripe

from cart.cart import Cart
from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from accounts.models import UserProfile
from .utils import send_order_confirmation_email, send_cancellation_confirmation_email, send_order_shipped_email


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
            order.status = 'processing'
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

    # Send order confirmation email only if not sent
    if not order.confirmation_email_sent:
        try:
            send_order_confirmation_email(order)
            order.confirmation_email_sent = True
            order.save()
        except Exception as e:
            messages.warning(
                request,
                'Order confirmation email could not be sent. '
                'Please check your order history for confirmation.'
            )

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


@login_required
def cancel_order(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)

    if request.method == 'POST':
        if order.status in ['pending', 'processing']:
            try:
                if order.status == 'pending':
                    # Immediate cancellation for pending orders
                    stripe.Refund.create(payment_intent=order.stripe_pid)
                    order.status = 'cancelled'
                    messages.success(
                        request,
                        'Order cancelled successfully. Refund will be processed.'
                    )
                else:
                    # Request cancellation for processing orders
                    order.status = 'cancellation_requested'
                    messages.success(
                        request,
                        'Cancellation request received. Staff will review it shortly.'
                    )
                order.save()
            except stripe.error.StripeError as e:
                messages.error(
                    request, 
                    'There was an error processing your refund. Please contact support.'
                )
        elif order.status == 'cancellation_requested':
            messages.info(request, 'Your cancellation request is being reviewed.')
        else:
            messages.error(request, 'This order cannot be cancelled.')
        return redirect('accounts:profile')

    return render(request, 'checkout/cancel_order.html', {'order': order})


@staff_member_required
def staff_orders(request):
    """Staff view to manage orders"""
    status = request.GET.get('status', 'cancellation_requested')
    orders = Order.objects.filter(status=status).order_by('-date')

    # Get counts for navigation
    cancellation_count = Order.objects.filter(
        status='cancellation_requested'
    ).count()

    context = {
        'orders': orders,
        'status': status,
        'cancellation_count': cancellation_count,
    }

    return render(request, 'checkout/staff_orders.html', context)


@staff_member_required
def approve_cancellation(request, order_number):
    """Approve an order cancellation request"""
    if request.method == 'POST':
        order = get_object_or_404(
            Order, 
            order_number=order_number,
            status='cancellation_requested'
        )
        try:
            # Process refund through Stripe
            stripe.api_key = settings.STRIPE_SECRET_KEY
            stripe.Refund.create(payment_intent=order.stripe_pid)
            order.status = 'cancelled'
            order.save()

            # Send cancellation confirmation email
            try:
                send_cancellation_confirmation_email(order)
            except Exception:
                messages.warning(
                    request,
                    'Cancellation email could not be sent, but refund was processed.'
                )

            messages.success(
                request,
                'Order cancellation approved and refund processed.'
            )
        except stripe.error.StripeError:
            messages.error(
                request,
                'Error processing refund. Please try again or contact support.'
            )
    return redirect('checkout:staff_orders') 


@login_required
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    # Check if user is authorized to view this order
    if request.user != order.user and not request.user.is_staff:
        messages.error(request, 'You are not authorized to view this order.')
        return redirect('home')

    template = 'checkout/order_detail.html'
    context = {
        'order': order,
    }

    return render(request, template, context)


def payment_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    if order.status == 'pending':
        order.status = 'processing'
        order.send_confirmation_email()  # Will only send if not already sent
        order.save()

    return redirect('checkout:order_detail', order_number=order_number)


@staff_member_required
def complete_order(request, order_number):
    """Mark an order as completed and send shipping notification"""
    if request.method == 'POST':
        order = get_object_or_404(
            Order,
            order_number=order_number,
            status='processing'
        )
        order.status = 'completed'
        order.save()

        try:
            send_order_shipped_email(order)
            messages.success(
                request, 
                f'Order {order_number} marked as completed and shipping notification sent.'
            )
        except Exception as e:
            messages.warning(
                request,
                'Order marked as completed but shipping notification failed to send.'
            )

    return redirect('checkout:staff_orders')
