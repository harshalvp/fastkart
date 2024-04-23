from decimal import Decimal

from django.conf import settings

CART_SESSION_KEY = getattr(settings, "CART_SESSION_KEY", "cart")


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_KEY)
        if not cart:
            cart = self.session[CART_SESSION_KEY] = {}
        self.cart = cart

    def add(self, product_variant, quantity=1):
        product_id = str(product_variant.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "sale_price": str(product_variant.sale_price),
            }
        self.cart[product_id]["quantity"] += quantity
        self.save()

    def remove(self, product_variant):
        product_id = str(product_variant.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def decrease_quantity(self, product_variant):
        product_id = str(product_variant.id)
        if product_id in self.cart and self.cart[product_id]["quantity"] > 1:
            self.cart[product_id]["quantity"] -= 1
            self.save()

    def save(self):
        self.session.modified = True

    def get_cart(self):
        return self.cart.items()

    def get_total_price(self, item):
        return Decimal(item["quantity"]) * Decimal(item["sale_price"])

    def cart_total(self):
        return sum(
            Decimal(item[1]["quantity"]) * Decimal(item[1]["sale_price"])
            for item in self.get_cart()
        )

    def get_product_quantity(self, product_variant):
        product_id = str(product_variant.id)
        item = self.cart.get(product_id)
        if item:
            return item["quantity"]
        return 0

    def clear(self):
        del self.session[CART_SESSION_KEY]
        self.save()
