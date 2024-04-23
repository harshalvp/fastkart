from django.contrib import admin
from .models import CartItem,  Order, OrderUpdate, Wishlist , OrderProduct
from .models import Coupon

# Register your models here.

class OrderInlines(admin.TabularInline):
    
    model = OrderProduct
    readonly_fields = ("product", "quantity", "price","total")
    can_delete = False
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["name", "user", "address", "status", "order_id"]
    list_filter = ["status", "timestamp"]
    search_fields = ["order_id", "user__username"]
    inlines=[OrderInlines]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("product","quantity",)
    search_fields = ("product__name",)




@admin.register(OrderUpdate)
class OrderUpdateAdmin(admin.ModelAdmin):
    list_display = ("order", "status", "timestamp")
    list_filter = ("status",)
    search_fields = ("status",)



@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("user", "product")
    search_fields = ("user__username", "product__name")



@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_amount', 'expiry_date', 'is_valid')
    search_fields = ('code',)
    list_filter = ('expiry_date',)