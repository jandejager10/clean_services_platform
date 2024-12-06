from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def send_order_confirmation_email(order):
    """Send order confirmation email with invoice to customer"""
    subject = f'Order Confirmation - {order.order_number}'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [order.email]

    context = {
        'order': order,
    }
    
    html_content = render_to_string(
        'checkout/emails/order_confirmation.html', context)

    send_mail(
        subject,
        '',  # Empty string for text content
        from_email,
        to_email,
        html_message=html_content,
        fail_silently=False,
    ) 

def send_cancellation_confirmation_email(order):
    """Send cancellation confirmation email to customer"""
    subject = f'Order Cancellation Confirmed - {order.order_number}'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [order.email]
    
    context = {
        'order': order,
    }
    
    html_content = render_to_string(
        'checkout/emails/cancellation_confirmation.html', context)
    
    send_mail(
        subject,
        '',
        from_email,
        to_email,
        html_message=html_content,
        fail_silently=False,
    ) 