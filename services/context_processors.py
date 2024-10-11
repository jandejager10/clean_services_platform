from .models import Category


def service_categories(request):
    return {
        'service_categories': Category.objects.all()
    }
