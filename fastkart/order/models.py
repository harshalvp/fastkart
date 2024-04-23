from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.utils import timezone

# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=150)
    phone=models.CharField(max_length=150)
    address = models.TextField()
    order_id = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=255,
        default="Pending",
        choices=(
            ("Pending", "Pending"),
            ("Processing", "Processing"),
            ("Delivered", "Delivered"),
            ("Cancelled", "Cancelled"),
        ),
    )
    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        
    def save(self, *args, **kwargs):
        if not self.order_id:
            last_order = Order.objects.order_by('-id').first()
            if last_order:
                last_order_id = int(last_order.order_id)
                new_order_id = max(1000, last_order_id + 1)
            else:
                new_order_id = 1000

            self.order_id = str(new_order_id)

        super().save(*args, **kwargs)

    def get_items(self):
        return CartItem.objects.filter(order=self)

    def get_updates(self):
        return OrderUpdate.objects.filter(order=self)
    
    def get_items(self):
        return CartItem.objects.filter(order=self)

    def get_updates(self):
        return OrderUpdate.objects.filter(order=self)

    def grand_total(self):
        return self.cart_total()
    
    def get_items(self):
        return OrderProduct.objects.filter(order=self)
    
    def calculate_subtotal(self):
        subtotal = 0.0
        order_products = self.orderproduct_set.all()  # Access related OrderProduct instances
        for order_product in order_products:
            subtotal += order_product.price * order_product.quantity
        return subtotal
    
    def get_billing_info(self):
        return f"{self.user.get_full_name()} - {self.user.email} - {self.user.phone}"

    def __str__(self):
        return str(self.user)
    

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.CharField(max_length=50)
    image=models.ImageField(upload_to='media/order_image')
    quantity = models.IntegerField()
    price = models.IntegerField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.product
    

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE)
    variant = models.CharField(max_length=100)
    sale_price = models.FloatField(blank=True, null=True)
    regular_price = models.FloatField(blank=True,null=True)
    quantity = models.PositiveIntegerField(default=1)
    is_offer_applied = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Cart Item")
        verbose_name_plural = _("Cart Items")
 
    def get_product_name(self):
        return self.product.name
    

    def get_total_price(self):
        total_price = 0
        for color in self.product.availablesize_set.all():
            sale_price = color.sale_price
            if color.regular_price:
                sale_price = color.sale_price - (color.sale_price * color.regular_price / 100)
            total_price += sale_price

        return total_price * self.quantity

    
    def cart_total(self):
        return float(sum(item.get_total_price() for item in CartItem.objects.filter(user=self.user)))

    def __str__(self):
        return f"{self.product} - {self.quantity}"


class OrderUpdate(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=255,
        choices=(
            ("", "- Select Status -"),
            ("Pending", "Placed"),
            ("Processing", "Confirmed"),
            ("Shipped", "Shipped"),
            ("Delivered", "Delivered"),
            ("Cancelled", "Cancelled"),
        ),
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Order Update")
        verbose_name_plural = _("Order Updates")

    def __str__(self):
        return f"{self.order} - {self.status}"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE)
    variant = models.CharField(max_length=100)
    price = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("user", "product")
        verbose_name = _("Wishlist Item")
        verbose_name_plural = _("Wishlist Items")

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateTimeField(default=timezone.now)

    def is_valid(self):
        return self.expiry_date > timezone.now()