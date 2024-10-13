from django.shortcuts import render
from django.template import Template, Context
from django.urls import reverse
from .models import FAQCategory, FAQItem


# Create your views here.
def faq_list(request):
    categories = FAQCategory.objects.all().prefetch_related('items')
    for category in categories:
        for item in category.items.all():
            template = Template(item.answer)
            context = Context({'request': request})
            item.rendered_answer = template.render(context)
    return render(request, 'faq/faq_list.html', {'categories': categories})
