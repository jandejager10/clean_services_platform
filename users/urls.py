from django.urls import path
from . import views
from .views import profile

urlpatterns = [
    path('profile/', profile, name='profile'),
]
