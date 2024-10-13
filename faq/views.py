from django.shortcuts import render
from .models import FAQCategory, FAQItem


# Create your views here.
def faq_list(request):
    categories = FAQCategory.objects.all().prefetch_related('items')
    return render(request, 'faq/faq_list.html', {'categories': categories})
