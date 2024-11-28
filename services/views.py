from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from .models import Service, Category


def all_services(request):
    """View to show all services, including sorting and search queries"""
    services = Service.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                services = services.order_by(sortkey)
            if sortkey == 'category':
                sortkey = 'category__name'
                services = services.order_by(sortkey)
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            services = services.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            services = services.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request, 
                    "You didn't enter any search criteria!"
                )
                return redirect(reverse('services'))
            
            queries = (
                Q(name__icontains=query) | 
                Q(description__icontains=query)
            )
            services = services.filter(queries)

    current_sorting = f'{sort}_{direction}' if sort and direction else None

    context = {
        'services': services,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'services/services.html', context)


def service_detail(request, service_id):
    """View to show individual service details"""
    service = get_object_or_404(Service, pk=service_id)

    context = {
        'service': service,
    }

    return render(request, 'services/service_detail.html', context)


def category_services(request, category_name):
    """View to show services in a specific category"""
    category = get_object_or_404(Category, name=category_name)
    services = Service.objects.filter(category=category)

    context = {
        'category': category,
        'services': services,
    }

    return render(request, 'services/category_services.html', context)


def residential_cleaning(request):
    """View to show residential cleaning services page"""
    context = {
        'residential_services': Service.objects.filter(
            category__name='home_cleaning'
        ).order_by('price')
    }
    return render(request, 'services/residential_cleaning.html', context)


def recurring_services(request):
    """View to show recurring services page"""
    context = {
        'recurring_services': Service.objects.filter(
            is_recurring=True
        ).order_by('price')
    }
    return render(request, 'services/recurring_services.html', context)


def commercial_cleaning(request):
    """View to show commercial cleaning services page"""
    context = {
        'commercial_services': Service.objects.filter(
            category__name='office_cleaning'
        ).order_by('price')
    }
    return render(request, 'services/commercial_cleaning.html', context) 