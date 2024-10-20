from decimal import Decimal
from django.conf import settings
from products.models import Product
import json


class Cart:
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        print(f"Cart initialized: {self.cart}")  # Debug print

    def save(self):
        """
        Save the cart in the session.
        """
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
        print(f"Cart saved: {self.cart}")  # Debug print

    def add(self, product, quantity=1, update_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price),
                'name': product.name
            }
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()
        print(f"Product added: {product_id}, Quantity: {quantity}")  # Debug print

    def get(self):
        """
        Get the cart.
        """
        return self.cart

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        
        for product in products:
            cart[str(product.id)]['product'] = {
                'id': product.id,
                'name': product.name,
                'price': str(product.price)
            }

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Get the total cost of the items in the cart.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """
        Remove the cart from the session.
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_subtotal(self):
        return self.get_total_price()

    def get_vat(self):
        return self.get_subtotal() * settings.VAT_RATE

    def get_total_with_vat(self):
        return self.get_subtotal() + self.get_vat()
