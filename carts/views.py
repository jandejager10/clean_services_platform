from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from products.models import Product
from .cart import Cart
from decimal import Decimal
from django.conf import settings


def cart_detail(request):
    cart = Cart(request)
    cart_items = []
    subtotal = Decimal('0.00')
    for item_id, item_data in cart.cart.items():
        product = Product.objects.get(id=item_id)
        item_total = Decimal(item_data['price']) * item_data['quantity']
        subtotal += item_total
        item = {
            'product': product,
            'quantity': item_data['quantity'],
            'price': Decimal(item_data['price']),
            'total_price': item_total
        }
        cart_items.append(item)
    
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
    return redirect('carts:cart_detail')  # Update this line


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
