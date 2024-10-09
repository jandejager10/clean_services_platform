from django.db import models

# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DurationField(blank=True, null=True)  # Optional duration for services

    def __str__(self):
        return self.name