from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('calendar/', views.booking_calendar, name='calendar'),
    path('create/<int:service_id>/', views.create_booking, name='create_booking'),
    path('detail/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('api/events/', views.get_calendar_events, name='calendar_events'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('staff/', views.staff_bookings, name='staff_bookings'),
    path('confirm/<int:booking_id>/', views.confirm_booking, name='confirm_booking'),
    path('reject/<int:booking_id>/', views.reject_booking, name='reject_booking'),
    path('request-cancellation/<int:booking_id>/', 
         views.request_booking_cancellation, 
         name='request_cancellation'),
] 