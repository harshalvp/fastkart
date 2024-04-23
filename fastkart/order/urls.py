from django.urls import path
from . import views

app_name = "order"


# URL patterns
urlpatterns = [
    # Wishlist
    path("wishlist/", views.WishlistListView.as_view(), name="wishlist"),
    path("shop/wishlist/add/",views.AddToWishlistView.as_view(),name="add_to_wishlist"),
    path("wishlist/remove/<int:product_id>/",views.RemoveFromWishlistView.as_view(),name="remove_from_wishlist"),
    
    path("cart/", views.CartView.as_view(), name="cart"),
    path("cart/add/<str:pk>/", views.AddToCartView.as_view(), name="add_to_cart"),
    path('shop/cart/minus/', views.MinusCartView.as_view(), name='minus_to_cart'),
    path("cart/remove/<int:cart_item_id>/",views.RemoveCartItemView.as_view(),name="remove_cart_item"),
    path('clear-cart/', views.ClearCartView.as_view(), name='clear_cart'),
    
    # path('apply-coupon/',  views.apply_coupon, name='apply_coupon'),
    
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("order-completed/", views.order_completed, name="order-completed"),
]