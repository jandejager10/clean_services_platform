from django.shortcuts import render
from .models import Service, Category


# Create your views here.
def service_list(request):
    services = Service.objects.all()
    categories = Category.objects.all()

    category = request.GET.get('category')
    if category:
        services = services.filter(category__name=category)

    context = {
        'services': services,
        'categories': categories,
        'current_category': category,
    }
    return render(request, 'services/service_list.html', context)


def residential_cleaning(request):
    return render(request, 'services/residential_cleaning.html')


def commercial_cleaning(request):
    return render(request, 'services/commercial_cleaning.html')


def recurring_services(request):
    return render(request, 'services/recurring_services.html')
