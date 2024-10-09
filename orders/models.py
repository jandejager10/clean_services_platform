from django.db import models

from products.models import Product  # Import the Product model
from services.models import Service  # Import the Service model

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(to='auth.User', on_delete=models.CASCADE)  # Link order to user
    products = models.ManyToManyField(Product, through='OrderItem')  # Many-to-Many relationship with products
    services = models.ManyToManyField(Service, through='OrderService')  # Many-to-Many relationship with services
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of order creation

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"  # Example order string

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class OrderService(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
