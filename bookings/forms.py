from django import forms
from .models import Booking, TimeSlot


class BookingForm(forms.ModelForm):
    """Form for creating and editing bookings"""
    class Meta:
        model = Booking
        fields = ['service', 'date', 'time_slot', 'frequency', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control' 