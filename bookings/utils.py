from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User


def send_booking_confirmation_email(booking):
    """Send booking confirmation email to user"""
    subject = f'Booking Confirmation - {booking.service.name}'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [booking.user.email]

    context = {
        'booking': booking,
        'user': booking.user,
    }
    
    html_content = render_to_string(
        'bookings/emails/booking_confirmation.html', context)

    send_mail(
        subject,
        '',  # Empty string for text content
        from_email,
        to_email,
        html_message=html_content,
        fail_silently=False,
    )


def send_booking_cancelled_email(booking):
    """Send booking cancellation email to user"""
    subject = f'Booking Cancelled - {booking.service.name}'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [booking.user.email]

    context = {
        'booking': booking,
        'user': booking.user,
    }
    
    html_content = render_to_string(
        'bookings/emails/booking_cancelled.html', context)

    send_mail(
        subject,
        '',  # Empty string for text content
        from_email,
        to_email,
        html_message=html_content,
        fail_silently=False,
    )


def send_booking_pending_email(booking):
    """Send booking pending notification to user"""
    subject = f'Booking Received - {booking.service.name}'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [booking.user.email]

    context = {
        'booking': booking,
        'user': booking.user,
    }
    
    html_content = render_to_string(
        'bookings/emails/booking_pending.html', context)

    send_mail(
        subject,
        '',  # Empty string for text content
        from_email,
        to_email,
        html_message=html_content,
        fail_silently=False,
    )


def send_cancellation_request_email(booking):
    """Send email to staff about cancellation request"""
    subject = f'Booking Cancellation Request - {booking.service.name}'
    from_email = settings.DEFAULT_FROM_EMAIL
    staff_emails = User.objects.filter(is_staff=True).values_list('email', flat=True)
    
    context = {
        'booking': booking,
        'user': booking.user,
    }
    
    html_content = render_to_string(
        'bookings/emails/cancellation_request.html', context)
    
    send_mail(
        subject,
        '',
        from_email,
        staff_emails,
        html_message=html_content,
        fail_silently=False,
    ) 