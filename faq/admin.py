from django.contrib import admin
from .models import FAQCategory, FAQItem


@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'created_at', 'updated_at')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    ordering = ('order', 'name')


@admin.register(FAQItem)
class FAQItemAdmin(admin.ModelAdmin):
    list_display = (
        'question',
        'category',
        'order',
        'is_active',
        'created_at',
        'updated_at'
    )
    list_editable = ('order', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('question', 'answer')
    ordering = ('category', 'order', 'question')
    raw_id_fields = ('category',) 