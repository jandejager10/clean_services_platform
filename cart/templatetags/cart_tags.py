from django import template
from decimal import Decimal
import decimal

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiply the value by the argument"""
    try:
        result = Decimal(str(value)) * Decimal(str(arg))
        return result.quantize(Decimal('0.01'))
    except (ValueError, TypeError, decimal.InvalidOperation):
        return 0 