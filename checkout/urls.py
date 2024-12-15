from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('success/<str:order_number>/', views.checkout_success, name='checkout_success'),
    path('cancel-order/<str:order_number>/', views.cancel_order, name='cancel_order'),
    path('staff/', views.staff_orders, name='staff_orders'),
    path('approve-cancellation/<str:order_number>/', views.approve_cancellation, name='approve_cancellation'),
    path('complete-order/<str:order_number>/', 
         views.complete_order, 
         name='complete_order'),
] 