from django.db import models
from django.conf import settings
from services.models import Service
from accounts.models import UserProfile


class TimeSlot(models.Model):
    """Model for available time slots"""
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"


class ServiceProvider(models.Model):
    """Model for service providers/staff"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    services = models.ManyToManyField(Service)
    is_available = models.BooleanField(default=True)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.user.get_full_name()


class Booking(models.Model):
    """Model for service bookings"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
        ('cancellation_requested', 'Cancellation Requested'),
    ]

    FREQUENCY_CHOICES = [
        ('one-off', 'One-off'),
        ('weekly', 'Weekly'),
        ('biweekly', 'Bi-weekly'),
        ('monthly', 'Monthly'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    provider = models.ForeignKey(ServiceProvider,
                                 on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES,
                              default='pending')
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES,
                                 default='one-off')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-time_slot__start_time']

    def __str__(self):
        return f"{self.service} - {self.date} {self.time_slot}"
