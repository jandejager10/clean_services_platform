from .models import Category

def categories(request):
    """
    Add service categories to context for all templates
    """
    return {
        'service_categories': Category.objects.all()
    } 