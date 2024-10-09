import os
from django.shortcuts import render

# Create your views here.
def index(request):
    print(os.path.abspath('home/templates/home/index.html'))
    return render(request, 'home/index.html')