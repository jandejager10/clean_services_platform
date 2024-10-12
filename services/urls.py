from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.service_list, name='service_list'),
    path('residential-cleaning/', views.residential_cleaning, name='residential_cleaning'),
    path('commercial-cleaning/', views.commercial_cleaning, name='commercial_cleaning'),
    path('recurring-services/', views.recurring_services, name='recurring_services'),
]
