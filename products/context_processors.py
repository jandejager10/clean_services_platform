from .models import Category

def categories(request):
    """
    Add product categories to context for all templates
    """
    return {
        'product_categories': Category.objects.all()
    } 