from django.urls import path
from . import views

app_name = 'promotions'

urlpatterns = [
    path('offers/', views.offers, name='offers'),
    # Add other URL patterns for the promotions app here
]
