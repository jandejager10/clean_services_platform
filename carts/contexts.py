from decimal import Decimal
from .cart import Cart
from products.models import Product


def cart_contents(request):
    cart = Cart(request)
    cart_items = []
    total = Decimal('0.00')
    product_count = 0
    
    for item_id, item_data in cart.cart.items():
        try:
            product = Product.objects.get(id=item_id)
            if isinstance(item_data, int):
                # This is a product without size
                quantity = item_data
            elif isinstance(item_data, dict):
                # This is a product with size or other attributes
                quantity = sum(int(value) for value in item_data.values() if value.isdigit())
            else:
                # Unexpected type, skip this item
                continue

            # Ensure price and quantity are the correct types
            price = Decimal(str(product.price))
            quantity = int(quantity)

            total += price * quantity
            product_count += quantity
            cart_items.append({
                'id': item_id,
                'quantity': quantity,
                'product': product,
            })
        except Product.DoesNotExist:
            # Handle case where product doesn't exist (maybe it was deleted)
            cart.remove(item_id)
            continue
        except (ValueError, TypeError, AttributeError):
            # Handle case where price or quantity can't be converted
            continue
    
    grand_total = total  # Add tax or shipping here if needed
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'grand_total': grand_total,
    }
    
    return context
