from django.urls import path
from . import views  # Import product views

app_name = 'products'  # Set the application namespace to 'products'

urlpatterns = [
    path('', views.all_products, name='product_list'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('<int:product_id>/delete/', views.delete_product, name='delete_product'),
]