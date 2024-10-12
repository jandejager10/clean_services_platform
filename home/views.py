import os
from django.shortcuts import render
from django.views import View


# Create your views here.
def index(request):
    print(os.path.abspath('home/templates/home/index.html'))
    return render(request, 'home/index.html')


def about(request):
    return render(request, 'home/about.html')


def contact(request):
    return render(request, 'home/contact.html')
