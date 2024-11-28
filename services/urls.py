from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.all_services, name='services'),
    path('residential/', views.residential_cleaning, name='residential_cleaning'),
    path('<int:service_id>/', views.service_detail, name='service_detail'),
    path('category/<str:category_name>/', views.category_services, name='category_services'),
    path('recurring/', views.recurring_services, name='recurring_services'),
    path('commercial/', views.commercial_cleaning, name='commercial_cleaning'),
] 