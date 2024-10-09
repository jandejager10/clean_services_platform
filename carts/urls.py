from django.urls import path
from . import views

app_name = 'carts'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),  # Main cart view
    path('<int:product_id>/add/', views.add_to_cart, name='add_to_cart'),
    path('<int:product_id>/remove/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.cart_checkout, name='cart_checkout'),
    path('checkout/success/', views.cart_checkout_success, name='cart_checkout_success'),
    path('checkout/cancel/', views.cart_checkout_cancel, name='cart_checkout_cancel'),
]