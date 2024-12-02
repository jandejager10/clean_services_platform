from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import time
from bookings.models import TimeSlot


class Command(BaseCommand):
    help = 'Create initial time slots'

    def handle(self, *args, **kwargs):
        # Define time slots (30-minute intervals from 8 AM to 8 PM)
        start_times = []
        current = time(8, 0)  # 8:00 AM
        end = time(20, 0)     # 8:00 PM

        while current < end:
            start_times.append(current)
            # Add 30 minutes
            hour = current.hour + ((current.minute + 30) // 60)
            minute = (current.minute + 30) % 60
            current = time(hour, minute)

        # Create time slots
        for start in start_times:
            # Calculate end time (30 minutes later)
            end_hour = start.hour + ((start.minute + 30) // 60)
            end_minute = (start.minute + 30) % 60
            end = time(end_hour, end_minute)

            TimeSlot.objects.get_or_create(
                start_time=start,
                end_time=end,
                defaults={'is_available': True}
            )

        self.stdout.write(self.style.SUCCESS('Successfully created time slots')) 