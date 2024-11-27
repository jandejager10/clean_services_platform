from django.shortcuts import render
from django.views.generic import ListView
from .models import FAQCategory, FAQItem


def faq_list(request):
    """View for displaying all FAQs organized by category"""
    categories = FAQCategory.objects.prefetch_related('faqitem_set').all()
    context = {
        'categories': categories,
    }
    return render(request, 'faq/faq_list.html', context)


def faq_category(request, category_id):
    """View for displaying FAQs from a specific category"""
    category = FAQCategory.objects.prefetch_related('faqitem_set').get(id=category_id)
    context = {
        'category': category,
        'faqs': category.faqitem_set.all(),
    }
    return render(request, 'faq/faq_category.html', context)


def faq_search(request):
    """View for searching FAQs"""
    query = request.GET.get('q', '')
    results = []
    
    if query:
        results = FAQItem.objects.filter(
            question__icontains=query
        ) | FAQItem.objects.filter(
            answer__icontains=query
        )
    
    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'faq/faq_search.html', context) 