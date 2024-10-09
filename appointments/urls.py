from django.urls import path
from . import views

urlpatterns = [
    path('appointments/', views.appointments, name='appointments'),
    # path('add/', views.add_appointment, name='add_appointment'),
]
# Compare this snippet from clean_services_platform/appointments/views.py:
# from django.shortcuts import render
# from .models import Appointment
#
# # Create your views here.
# def appointments(request):
#     appointments = Appointment.objects.all()
#     return render(request, 'appointments/appointments.html', {'appointments': appointments})
#
# def add_appointment(request):
#     return render(request, 'appointments/add_appointment.html')
# Compare this snippet from clean_services_platform/appointments/models.py:
# from django.db import models
# from django.contrib.auth.models import User
# from services.models import Service
# from datetime import datetime
#
# # Create your models here.
# class Appointment
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     service = models.ForeignKey(Service, on_delete=models.CASCADE)
#     date = models.DateField()
#     time = models.TimeField()
#     confirmed = models.BooleanField(default=False)
#
#     def __str__(self):
#         return f"Appointment for {self.user.username} - {self.service.name} on {self.date} at {self.time}"
#
#     def is_past_due(self):
#         now = datetime.now()
#         return datetime.combine(self.date, self.time) < now
# Compare this snippet from clean_services_platform/appointments/urls.py:
# from django.urls import path
# from . import views
#   
# urlpatterns = [
#     path('appointments/', views.appointments, name='appointments'),
#     path('add/', views.add_appointment, name='add_appointment'),
# ]
# Compare this snippet from clean_services_platform/appointments/views.py:
# from django.shortcuts import render
# from .models import Appointment
#
# # Create your views here.
# def appointments(request):
#     appointments = Appointment.objects.all()
#     return render(request, 'appointments/appointments.html', {'appointments': appointments})
#
# def add_appointment(request):
#     return render(request, 'appointments/add_appointment.html')
# Compare this snippet from clean_services_platform/appointments/models.py:
# from django.db import models
# from django.contrib.auth.models import User
# from services.models import Service
# from datetime import datetime
#
# # Create your models here.
# class Appointment
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     service = models.ForeignKey(Service, on_delete=models.CASCADE)
#     date = models.DateField()
#     time = models.TimeField()
#     confirmed = models.BooleanField(default=False)
#
#     def __str__(self):
#         return f"Appointment for {self.user.username} - {self.service.name} on {self.date} at {self.time}"
#
#     def is_past_due(self):
#         now = datetime.now()
#         return datetime.combine(self.date, self.time) < now
# Compare this snippet from clean_services_platform/appointments/urls.py:
# from django.urls import path
# from . import views
#
# urlpatterns = [
#     path('appointments/', views.appointments, name='appointments'),
#     path('add/', views.add_appointment, name='add_appointment'),
# ]
# Compare this snippet from clean_services_platform/appointments/views.py:
# from django.shortcuts import render
# from .models import Appointment
#
# # Create your views here.
# def appointments(request):
#     appointments = Appointment.objects.all()
#     return render(request, 'appointments/appointments.html', {'appointments': appointments})
#
# def add_appointment(request):
#     return render(request, 'appointments/add_appointment.html')
# Compare this snippet from clean_services_platform/appointments/models.py:
# from django.db import models
# from django.contrib.auth.models import User
# from services.models import Service
# from datetime import datetime
#
# # Create your models here.
# class Appointment
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     service = models.ForeignKey(Service, on_delete=models.CASCADE)
#     date = models.DateField()
#     time = models.TimeField()
#     confirmed = models.BooleanField(default=False)
#
#     def __str__(self):
#         return f"Appointment for {self.user.username} - {self.service.name} on {self.date} at {self.time}"
#
#     def is_past_due(self):
#         now = datetime.now()
#         return datetime.combine(self.date, self.time) < now
# Compare this snippet from clean_services_platform/appointments/urls.py:
# from django.urls import path
# from . import views
#
# urlpatterns = [
#     path('appointments/', views.appointments, name='appointments'),
#     path('add/', views.add_appointment, name='add_appointment'),
# ]
# Compare this snippet from clean_services_platform/appointments/views.py:
# from django.shortcuts import render
# from .models import Appointment
#
# # Create your views here.
# def appointments(request):
#     appointments = Appointment.objects.all()
#     return render(request, 'appointments/appointments.html', {'appointments': appointments})
#
# def add_appointment(request):
#     return render(request, 'appointments/add_appointment.html')
# Compare this snippet from clean_services_platform/appointments/models.py:
# from django.db import models
# from django.contrib.auth.models import User
# from services.models import Service
# from datetime import datetime
#
