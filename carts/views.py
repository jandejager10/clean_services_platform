from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from products.models import Product
from .cart import Cart  # Import the Cart class


# Create your views here.
def cart_detail(request):
    """A view to display the cart details."""
    cart = Cart(request)
    context = {
        'cart': cart,
    }
    return render(request, 'carts/cart_detail.html', context)


@login_required
def add_to_cart(request, product_id):
    """Add a product to the cart."""
    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get('quantity', 1))
    redirect_url = request.POST.get('redirect_url')
    cart = Cart(request)

    cart.add(product=product, quantity=quantity)
    messages.success(request, f'Added {product.name} to your cart.')
    return redirect(redirect_url)


@login_required
def remove_from_cart(request, product_id):
    """Remove a product from the cart."""
    product = get_object_or_404(Product, pk=product_id)
    cart = Cart(request)

    cart.remove(product)
    messages.success(request, f'Removed {product.name} from your cart.')
    return redirect('carts:cart_detail')


@login_required
def cart_checkout(request):
    """View to handle the cart checkout process."""
    cart = Cart(request)

    if request.method == 'POST':
        # Logic for processing the checkout (e.g., handling payment)
        # Placeholder for actual checkout processing
        return redirect('carts:cart_checkout_success')

    context = {
        'cart': cart,
    }
    return render(request, 'carts/cart_checkout.html', context)


@login_required
def cart_checkout_success(request):
    """View to display a success message after checkout."""
    cart = Cart(request)
    cart.clear()  # Clear the cart after successful checkout
    messages.success(request, 'Your order was successful. Thank you for shopping with us!')

    return render(request, 'carts/cart_checkout_success.html')


@login_required
def cart_checkout_cancel(request):
    """View to handle checkout cancellation."""
    messages.warning(request, 'Your checkout has been cancelled.')
    return redirect('carts:cart_detail')