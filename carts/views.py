from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from products.models import Product
from .cart import Cart
from decimal import Decimal
from django.conf import settings
from django.http import JsonResponse
from .contexts import cart_contents


def cart_detail(request):
    cart = Cart(request)
    cart_items = list(cart)
    subtotal = sum(Decimal(item['price']) * item['quantity'] for item in cart_items)
    vat = subtotal * settings.VAT_RATE
    total_with_vat = subtotal + vat
    
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'vat': vat,
        'total_with_vat': total_with_vat,
    }
    return render(request, 'carts/cart_detail.html', context)


@require_POST
def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product=product, quantity=quantity)
    context = cart_contents(request)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'grand_total': '{:.2f}'.format(context['grand_total']),
            'product_count': context['product_count']
        })
    return redirect('carts:cart_detail')


@require_POST
def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('carts:cart_detail')


@require_POST
def update_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity'))
    cart.add(product=product, quantity=quantity, update_quantity=True)
    return redirect('carts:cart_detail')
