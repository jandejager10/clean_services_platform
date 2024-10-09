from django.shortcuts import render
from .models import Service

# Create your views here.
def service_list(request):
    return render(request, 'services/service_list.html')