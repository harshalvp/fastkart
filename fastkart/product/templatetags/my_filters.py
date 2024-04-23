from django import template

register = template.Library()

@register.filter(name='discount_price')
def discount_price(original_price, regular_price):
    return original_price - (original_price * regular_price / 100)


# @register.filter
# def discount_price(original_price, discount):
#     if original_price is None or discount is None:
#         return None  # or any default value you prefer

#     return original_price - (original_price * discount / 100)