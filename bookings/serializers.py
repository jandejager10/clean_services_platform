from rest_framework import serializers
from .models import Booking, TimeSlot


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'service', 'date', 'time_slot', 'status']


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['id', 'start_time', 'end_time', 'is_available'] 