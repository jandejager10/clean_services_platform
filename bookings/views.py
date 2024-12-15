from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .models import Booking, TimeSlot, ServiceProvider
from .forms import BookingForm
from services.models import Service
from django.http import JsonResponse
from datetime import datetime, timedelta
from .utils import send_booking_confirmation_email, send_booking_cancelled_email, send_booking_pending_email
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


@login_required
def booking_calendar(request):
    """Display available booking slots"""
    services = Service.objects.all()
    context = {
        'services': services,
    }
    return render(request, 'bookings/calendar.html', context)


@login_required
def create_booking(request, service_id):
    """Create a new booking"""
    service = get_object_or_404(Service, id=service_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.service = service
            
            # Assign available service provider
            provider = ServiceProvider.objects.filter(
                services=service, is_available=True).first()
            if provider:
                booking.provider = provider
            
            booking.save()
            
            # Send pending notification with error logging
            try:
                send_booking_pending_email(booking)
                messages.success(
                    request, 
                    'Booking request received! We will confirm it shortly.'
                )
            except Exception as e:
                print(f"Email sending failed: {str(e)}")  # For debugging
                messages.warning(
                    request, 
                    f'Booking created but notification email failed: {str(e)}'
                )
            
            return redirect('bookings:booking_detail', booking.id)
    else:
        form = BookingForm(initial={'service': service})

    context = {
        'form': form,
        'service': service,
    }
    return render(request, 'bookings/create_booking.html', context)


@login_required
def booking_detail(request, booking_id):
    """Display booking details"""
    if request.user.is_staff:
        # Staff can view any booking
        booking = get_object_or_404(Booking, id=booking_id)
    else:
        # Regular users can only view their own bookings
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    context = {
        'booking': booking,
    }
    return render(request, 'bookings/booking_detail.html', context)


@login_required
def my_bookings(request):
    """Display user's bookings"""
    bookings = Booking.objects.filter(user=request.user)
    context = {
        'bookings': bookings,
    }
    return render(request, 'bookings/my_bookings.html', context)


def get_calendar_events(request):
    """Return events for the calendar"""
    start = request.GET.get('start')
    end = request.GET.get('end')
    
    # Convert to datetime objects
    start_date = datetime.fromisoformat(start.replace('Z', '+00:00'))
    end_date = datetime.fromisoformat(end.replace('Z', '+00:00'))
    
    # Get bookings in date range
    if request.user.is_staff:
        # Staff can see all bookings
        bookings = Booking.objects.filter(
            date__range=[start_date.date(), end_date.date()]
        ).select_related('time_slot', 'service', 'user')
    else:
        # Users can only see their own bookings
        bookings = Booking.objects.filter(
            date__range=[start_date.date(), end_date.date()],
            user=request.user
        ).select_related('time_slot', 'service')
    
    # Format events for FullCalendar
    events = []
    for booking in bookings:
        title_parts = [booking.service.name]
        if request.user.is_staff:
            title_parts.append(f"({booking.user.get_full_name()})")
        title_parts.append(f"[{booking.status.upper()}]")
        
        events.append({
            'id': booking.id,
            'title': " ".join(title_parts),
            'start': f"{booking.date}T{booking.time_slot.start_time}",
            'end': f"{booking.date}T{booking.time_slot.end_time}",
            'backgroundColor': get_status_color(booking.status),
            'className': f'status-{booking.status}',
            'extendedProps': {
                'status': booking.status,
                'customer': booking.user.get_full_name() if request.user.is_staff else None
            }
        })
    
    return JsonResponse(events, safe=False)


def get_status_color(status):
    """Return color based on booking status"""
    colors = {
        'pending': '#ffc107',    # Warning yellow
        'confirmed': '#28a745',  # Success green
        'cancelled': '#dc3545',  # Danger red
        'completed': '#6c757d',  # Secondary gray
    }
    return colors.get(status, '#007bff')  # Default blue


@login_required
def cancel_booking(request, booking_id):
    """Cancel a booking"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if request.method == 'POST':
        if booking.status == 'pending':
            booking.status = 'cancelled'
            booking.save()
            
            try:
                send_booking_cancelled_email(booking)
                messages.success(
                    request,
                    'Booking cancelled successfully. A confirmation email has been sent.'
                )
            except Exception:
                messages.success(
                    request,
                    'Booking cancelled successfully, but email notification failed.'
                )
        else:
            messages.error(request, 'This booking cannot be cancelled.')
        
        return redirect('bookings:my_bookings')
    
    return redirect('bookings:booking_detail', booking_id=booking_id)


@staff_member_required
def staff_bookings(request):
    """Staff view to manage bookings"""
    status = request.GET.get('status', 'pending')
    bookings = Booking.objects.filter(status=status).order_by('date', 'time_slot')
    
    # Get counts for navigation
    pending_count = Booking.objects.filter(status='pending').count()
    cancellation_count = Booking.objects.filter(
        status='cancellation_requested'
    ).count()
    
    context = {
        'bookings': bookings,
        'status': status,
        'pending_count': pending_count,
        'cancellation_count': cancellation_count,
    }
    
    return render(request, 'bookings/staff_bookings.html', context)


@staff_member_required
def confirm_booking(request, booking_id):
    """Confirm a pending booking"""
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=booking_id, status='pending')
        booking.status = 'confirmed'
        booking.save()
        
        # Send confirmation email
        try:
            send_booking_confirmation_email(booking)
            messages.success(request, 'Booking confirmed and email sent.')
        except Exception:
            messages.warning(
                request, 
                'Booking confirmed but confirmation email failed to send.'
            )
        
    return redirect('bookings:staff_bookings')


@staff_member_required
def reject_booking(request, booking_id):
    """Reject a pending booking or approve a cancellation request"""
    if request.method == 'POST':
        booking = get_object_or_404(
            Booking, 
            id=booking_id, 
            status__in=['pending', 'cancellation_requested']
        )
        
        # If it's a cancellation request, handle it differently
        if booking.status == 'cancellation_requested':
            booking.status = 'cancelled'
            booking.save()
            try:
                send_booking_cancelled_email(booking)
                messages.success(
                    request, 
                    'Cancellation request approved and customer notified.'
                )
            except Exception:
                messages.warning(
                    request, 
                    'Cancellation approved but notification failed to send.'
                )
            return redirect('bookings:staff_bookings')
        
        # Handle regular rejection of pending booking
        booking.status = 'cancelled'
        booking.save()
        
        # Send cancellation email
        try:
            send_booking_cancelled_email(booking)
            messages.success(request, 'Booking rejected and email sent.')
        except Exception:
            messages.warning(
                request, 
                'Booking rejected but notification email failed to send.'
            )
        
    return redirect('bookings:staff_bookings')


@login_required
def request_booking_cancellation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if booking.status == 'confirmed':
        booking.status = 'cancellation_requested'
        booking.save()
        
        try:
            # Send email to customer
            subject = 'Booking Cancellation Request Received'
            html_message = render_to_string(
                'bookings/emails/cancellation_request_received.html',
                {
                    'booking': booking,
                    'user': request.user,
                }
            )
            
            send_mail(
                subject=subject,
                message='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            messages.success(
                request,
                'Your cancellation request has been submitted and is pending review.'
            )
        except Exception as e:
            messages.warning(
                request,
                'Cancellation request received but email notification failed. '
                'Please check your email settings.'
            )
            
        return redirect('bookings:booking_detail', booking_id=booking_id)
    else:
        messages.error(request, 'Only confirmed bookings can be cancelled.')
        return redirect('bookings:booking_detail', booking_id=booking_id)
  