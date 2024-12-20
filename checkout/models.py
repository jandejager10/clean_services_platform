import uuid
from django.db import models
from django.conf import settings
from products.models import Product
from accounts.models import UserProfile
from decimal import Decimal


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('cancellation_requested', 'Cancellation Requested'),
        ('refunded', 'Refunded'),
    ]
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    county = models.CharField(max_length=80, null=True, blank=True)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    tax = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    stripe_pid = models.CharField(
        max_length=254, null=False, blank=False, default=''
    )
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='pending'
    )
    confirmation_email_sent = models.BooleanField(default=False)

    def _generate_order_number(self):
        """Generate a random, unique order number using UUID"""
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """Update total when a line item is added"""
        self.subtotal = self.lineitems.aggregate(
            models.Sum('lineitem_total'))['lineitem_total__sum'] or 0
        self.tax = self.subtotal * Decimal(str(settings.TAX_RATE))
        self.total = self.subtotal + self.tax
        self.save()

    def save(self, *args, **kwargs):
        """Override the original save method to set the order number"""
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number

    def get_subtotal(self):
        """Calculate order subtotal"""
        return sum(item.line_total for item in self.lineitems.all())

    def get_tax(self):
        """Calculate tax amount"""
        return self.get_subtotal() * Decimal('0.20')

    def get_total(self):
        """Calculate total including tax"""
        return self.get_subtotal() + self.get_tax()

    def send_confirmation_email(self):
        """Send the confirmation email if not already sent"""
        if not self.confirmation_email_sent:
            # Send email logic here
            self.confirmation_email_sent = True
            self.save()


class OrderLineItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='lineitems'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE
    )
    quantity = models.IntegerField(default=0)
    lineitem_total = models.DecimalField(
        max_digits=6, decimal_places=2, editable=False
    )

    def save(self, *args, **kwargs):
        """Override the original save method to set the lineitem total"""
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'
