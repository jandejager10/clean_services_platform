from django.shortcuts import render
from . import views


# Create your views here.
def appointments(request):
    return render(request, 'appointments/appointments.html')