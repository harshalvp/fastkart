from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from product.models import AvailableSize
from .models import CartItem, Coupon
from order.models import OrderProduct
import urllib.parse 
from .forms import OrderForm
from django.views.generic.edit import FormView
from order.models import Wishlist
from product.models import Product
from django.template.loader import render_to_string
from django.views.generic import ListView
from order.cart import Cart
from .models import Coupon

# Create your views here.
# Wishlist
class WishlistListView(LoginRequiredMixin, ListView):
    model = Wishlist
    template_name = "web/wishlist.html"
    context_object_name = "wishlist_items"
    paginate_by = 10

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

                                      
class AddToWishlistView( View):
    def get(self, request ):
        if not request.user.is_authenticated:
            return JsonResponse({'message': 'User not authenticated'}, status=401)
        user = self.request.user
        product_id = request.GET.get("product_id",'')
        product = get_object_or_404(Product, pk=product_id)
        if not Wishlist.objects.filter(user=user, product=product).exists():
            # Create a new Wishlist object
            Wishlist.objects.create(
                user=user,
                product=product
            )
            wishlist_count = Wishlist.objects.filter(user=request.user).count()
            return JsonResponse({'message': 'Product Added from Wishlist successfully',
                                 'wishlist_count': wishlist_count})
        else:
            return JsonResponse({'message': 'Product is already in the Wishlist.'})


class RemoveFromWishlistView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        product_id = self.kwargs.get("product_id")
        user = self.request.user

        wishlist_item = get_object_or_404(Wishlist, user=user, id=product_id)
        wishlist_item.delete()

        wishlist_count = Wishlist.objects.filter(user=request.user).count()
        return JsonResponse({'message': 'Product Removed from Wishlist successfully', 'wishlist_count': wishlist_count})


class CartView(LoginRequiredMixin, View):
    template_name = "web/cart.html"

    def get(self, request, *args, **kwargs):
        user = self.request.user
        cart_items = CartItem.objects.filter(user=user)
        total = 0
        for item in cart_items:
            total += item.get_total_price()

        return render(request, self.template_name, {"cart_items": cart_items, "total": total,})
    

class AddToCartView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        user = self.request.user
        harshal = get_object_or_404(AvailableSize, pk=pk)
        product = harshal.color_product  # Assuming color_product is the related Product instance

        quantity = int(request.GET.get("quantity", 1))
        regular_price = harshal.sale_price

        cart_item, created = CartItem.objects.get_or_create(
            user=user,
            product=product,
            defaults={"quantity": quantity, "sale_price": harshal.sale_price, "regular_price": regular_price}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        cart_items_count = CartItem.objects.filter(user=user).count()

        response_data = {
            'success': True,
            'message': 'Item added to the cart successfully.',
            'cart_items_count': cart_items_count,
            'product_grand_price': cart_item.get_total_price(),
            'sub_total': cart_item.cart_total(),
            'quantity': cart_item.quantity,
        }

        return JsonResponse(response_data)


class MinusCartView(View):
   def get(self, request):
        try:
            cart_id = request.GET.get("cart_id")
            cart_item = CartItem.objects.get(id=cart_id)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            return JsonResponse({'message': 'Product Quantity Decreased in cart successfully', "product_grand_price": cart_item.get_total_price(), "sub_total": cart_item.cart_total(),'quantity':cart_item.quantity})

        except CartItem.DoesNotExist:
            return JsonResponse({'message': 'Product not found in cart'}, status=404)
        

class RemoveCartItemView(LoginRequiredMixin, View):
    def get(self, request, cart_item_id, *args, **kwargs):
        user = self.request.user
        cart_item = get_object_or_404(CartItem, id=cart_item_id, user=user)
        cart_item.delete()

        total = 0
        for item in CartItem.objects.filter(user=user):
            total += item.get_total_price()

        cart_items_count = CartItem.objects.filter(user=user).count()

        response_data = {
            'success': True,
            'message': 'Item removed from the cart successfully.',
            'cart_items_count': cart_items_count,
            'total': total,
        }

        return JsonResponse(response_data)


class ClearCartView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        CartItem.objects.filter(user=user).delete()
        return redirect("order:cart")





class CheckoutView(LoginRequiredMixin, FormView):
    template_name = "web/checkout.html"
    form_class = OrderForm
    
    def form_valid(self, form):
        order = form.save(commit=False)
        order.user = self.request.user
        order.save()

        cart_items = CartItem.objects.filter(user=self.request.user)


        products = ""
        total = 0
        counter = 1

        for cart_item in cart_items:
            for color in cart_item.product.availablesize_set.all():
                # Check if price and discount are not None
                if color.sale_price is not None and color.regular_price is not None:
                    # Calculate discounted price here
                    price = color.sale_price - (color.sale_price * color.regular_price / 100)
                else:
                    # Set a default value or skip the calculation
                    price = 0
            OrderProduct.objects.create(
                order=order,
                product=f"{cart_item.product.name}",
                image=str(cart_item.product.image),
                quantity=cart_item.quantity,
                price=price,
                total=cart_item.get_total_price(),
            )
            products += (
                f"{counter}.{cart_item.product.name}"
                f"({cart_item.quantity} \n ----------------------- \n"
            )
            total += cart_item.quantity 
            counter += 1


        message = (
            f"{products}\n "
            f"============================\n"
            f"Grand Total: {total}\n"
            f"Order Number: {order.order_id}\n"
            f"Purchase: Home Delivery \n"
            f"Name: {form.cleaned_data['name']}\n"
            f"Phone: {form.cleaned_data['phone']}\n"
            f"Address: {form.cleaned_data['address']}\n"
            f"============================\n"
            f"Final bill will be based on the product availability and amount derived there upon."
        )

        whatsapp_api_url = "https://api.whatsapp.com/send"
        phone_number = "919074212751"
        encoded_message = urllib.parse.quote(message)
        whatsapp_url = f"{whatsapp_api_url}?phone={phone_number}&text={encoded_message}"

        cart_items.delete()

        # return redirect(whatsapp_url)
        return redirect("order:order-completed")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve user's cart items and calculate total
        user = self.request.user
        cart_items = CartItem.objects.filter(user=user)
        cart_count = CartItem.objects.filter(user=user).count()
        wishlist_items = Wishlist.objects.filter(user=self.request.user)
        wishlist_items_count = wishlist_items.count()
        context["cart_items"] = cart_items
        context["cart_count"] = cart_count
        context['wishlist_items_count'] = wishlist_items_count
        total = 0

        for item in cart_items:
            total += item.get_total_price()

        context["total"] = total
        return context


def order_completed(request):
    return render(request, "web/order-completed.html")


def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')  # Assuming you're using POST method for form submission
        try:
            coupon = Coupon.objects.get(code=coupon_code)
            if coupon.is_valid():
                
                total_amount = request.session.get('total_amount', 0)
                discount_amount = coupon.discount_amount
                updated_total_amount = total_amount - discount_amount
                request.session['total_amount'] = updated_total_amount
                return render(request, 'cart.html', {'message': 'Coupon applied successfully'})
            else:
                return render(request, 'cart.html', {'error': 'Coupon is expired'})
        except Coupon.DoesNotExist:
            return render(request, 'cart.html', {'error': 'Invalid coupon code'})
    else:
        return render(request, 'cart.html')