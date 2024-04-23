from django.conf import settings
from order.models import Wishlist
from order.models import CartItem


def main_context(request):
    wishlist_count = Wishlist.objects.filter(user=request.user.id).count()

    cart_count = CartItem.objects.filter(user=request.user.id).count()


    return {
        "wishlist_count": wishlist_count,
        'cart_count': cart_count, 
        "domain": request.META["HTTP_HOST"],
        "current_version": "?v=2.0",
    }
