from django import template

register = template.Library()

@register.filter(name='in_cart')
def in_cart(row, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == row.id:
            return True
    return False

@register.filter(name='cart_quantity')
def cart_quantity(row, cart):
    for id ,value in cart.items():
        if int(id) == row.id:
            return value.get('quantity')
    return 0

