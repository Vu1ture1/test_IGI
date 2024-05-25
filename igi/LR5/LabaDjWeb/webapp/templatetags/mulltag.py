from django import template
from decimal import Decimal

register = template.Library()

@register.simple_tag()
def multiply(qty, unit_price, *args, **kwargs):
    var = Decimal(qty) * Decimal(unit_price)
    return round(var, 2)