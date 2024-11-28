from django.contrib import admin
from .models import Category, Service


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('friendly_name', 'name')
    search_fields = ('name', 'friendly_name')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'rating', 'is_recurring')
    list_filter = ('category', 'is_recurring', 'frequency')
    search_fields = ('name', 'description')
    ordering = ('category', 'name') 