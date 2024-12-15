from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    save_info = forms.BooleanField(
        required=False,
        initial=True,
        label='Update my profile with this delivery information',
        help_text='Check this box to update your saved delivery information'
    )

    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'county', 'postcode',)

    def __init__(self, *args, **kwargs):
        """Add placeholders and classes, remove auto-generated labels"""
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'town_or_city': 'Town or City',
            'county': 'County',
            'postcode': 'Postal Code',
        }

        # Only apply placeholders to non-save_info fields
        for field_name, field in self.fields.items():
            if field_name != 'save_info':
                if field.required:
                    placeholder = f'{placeholders[field_name]} *'
                else:
                    placeholder = placeholders[field_name]
                field.widget.attrs['placeholder'] = placeholder
                field.label = False
            else:
                field.widget.attrs['class'] = 'form-check-input mt-2'
