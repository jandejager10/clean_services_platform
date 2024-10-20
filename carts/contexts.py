from decimal import Decimal
from .cart import Cart
from products.models import Product
from django.conf import settings


def cart_contents(request):
    cart = Cart(request)
    cart_items = []
    total = Decimal('0.00')
    product_count = 0
    
    for item in cart:
        total += item['price'] * item['quantity']
        product_count += item['quantity']
        cart_items.append(item)

    subtotal = total
    vat = subtotal * settings.VAT_RATE
    grand_total = subtotal + vat
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'subtotal': subtotal,
        'vat': vat,
        'grand_total': grand_total,
    }
    
    return context
