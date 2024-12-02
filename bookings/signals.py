from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Booking
from .utils import send_booking_confirmation_email


@receiver(post_save, sender=Booking)
def booking_post_save(sender, instance, created, **kwargs):
    """Send confirmation email when booking is created"""
    if created:
        try:
            send_booking_confirmation_email(instance)
        except Exception:
            # Log error but don't prevent booking creation
            pass 