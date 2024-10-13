from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    friendly_name = models.CharField(max_length=255)

    def __str__(self):
        return self.friendly_name


class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DurationField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='services')
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)

    def __str__(self):
        return self.name
