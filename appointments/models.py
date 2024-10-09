from django.db import models
from datetime import datetime

from services.models import Service  # Import the Service model


# Create your models here.
class Appointment(models.Model):
    user = models.ForeignKey(to='auth.User', on_delete=models.CASCADE)  # Link appointment to user
    service = models.ForeignKey(Service, on_delete=models.CASCADE)  # Link appointment to service
    date = models.DateField()
    time = models.TimeField()
    confirmed = models.BooleanField(default=False)  # Flag to indicate appointment confirmation

    def __str__(self):
        return f"Appointment for {self.user.username} - {self.service.name} on {self.date} at {self.time}"  # Example appointment string

    def is_past_due(self):
        now = datetime
        return datetime.combine(self.date, self.time) < now
