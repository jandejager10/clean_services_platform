from decimal import Decimal, ROUND_HALF_UP
from django.conf import settings
from products.models import Product


class Cart:
    def __init__(self, request):
        """Initialize the cart."""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """Add a product to the cart or update its quantity."""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """Mark session as modified."""
        self.session.modified = True

    def remove(self, product):
        """Remove a product from the cart."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_subtotal_price(self):
        """Calculate total price before tax."""
        subtotal = Decimal('0.00')
        for item in self.cart.values():
            subtotal += Decimal(str(item['price'])) * item['quantity']
        return subtotal.quantize(Decimal('.01'), rounding=ROUND_HALF_UP)

    def get_tax(self):
        """Calculate tax amount."""
        if not self.cart:
            return Decimal('0.00')
        tax = self.get_subtotal_price() * Decimal(str(settings.TAX_RATE))
        return tax.quantize(Decimal('.01'), rounding=ROUND_HALF_UP)

    def get_delivery_cost(self):
        """Calculate delivery cost based on total"""
        subtotal = self.get_subtotal()
        if subtotal >= Decimal('50.00'):
            return Decimal('0.00')
        return Decimal('3.00')

    def get_total_price(self):
        """Calculate total price including tax and delivery"""
        if not self.cart:
            return Decimal('0.00')
        subtotal = self.get_subtotal_price()
        tax = self.get_tax()
        delivery = self.get_delivery_cost()
        total = subtotal + tax + delivery
        return total.quantize(Decimal('.01'), rounding=ROUND_HALF_UP)

    def clear(self):
        """Remove cart from session."""
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def __iter__(self):
        """Iterate over items in cart and get products from database."""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Count all items in the cart."""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total(self):
        return sum(item['total_price'] for item in self)

    def get_subtotal(self):
        return sum(item['total_price'] for item in self)

    def get_tax(self):
        return self.get_subtotal() * Decimal('0.20')
 