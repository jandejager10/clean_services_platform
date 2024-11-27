from django.urls import path
from . import views

app_name = 'faq'

urlpatterns = [
    path('', views.faq_list, name='faq_list'),
    path('category/<int:category_id>/', views.faq_category, name='faq_category'),
    path('search/', views.faq_search, name='faq_search'),
] 