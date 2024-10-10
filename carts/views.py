from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from products.models import Product  # Replace with your actual product model import
from .cart import Cart
from utils import DecimalEncoder
import json


@require_POST
def add_to_cart(request, product_id):  # Changed from cart_add to add_to_cart
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product=product, quantity=quantity)
    return redirect('carts:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    cart_items = []
    for item in cart:
        item_data = {
            'product': item['product'],
            'quantity': item['quantity'],
            'price': str(item['price']),
            'total_price': str(item['total_price'])
        }
        cart_items.append(item_data)
    
    context = {
        'cart_items': cart_items,
        'total': str(cart.get_total_price())
    }
    return render(request, 'carts/cart_detail.html', context)


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('carts:cart_detail')


@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        cart.add(product=product, quantity=quantity, override_quantity=True)
    else:
        cart.remove(product)
    return redirect('carts:cart_detail')