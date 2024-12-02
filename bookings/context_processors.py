from .models import Booking

def pending_bookings(request):
    """Add pending bookings count to context for staff members"""
    if request.user.is_staff:
        pending_count = Booking.objects.filter(status='pending').count()
        return {'pending_bookings_count': pending_count}
    return {} 