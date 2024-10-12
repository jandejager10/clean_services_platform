from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('appointments/', views.appointments, name='appointments'),
    path('add/<int:service_id>/', views.add_appointment, name='add_appointment'),
    path('confirm/<int:appointment_id>/', views.confirm_appointment, name='confirm_appointment'),
    path('cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
]
