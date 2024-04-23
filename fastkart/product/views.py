from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import DetailView
from .models import Product
from .models import Category,Subcategory
from django.template.loader import render_to_string




# Create your views here.

def index(request):
    new = Product.objects.filter(new_arrival=True)
    categories = Category.objects.all()
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        product = Product.objects.filter(category=category)
    context = {
        'categories': categories,
        'new': new,
    }
    return render(request, "web/index.html", context)  


def shop(request, category_slug=None, subcategory_slug=None):
    product = Product.objects.all()
    categories = Category.objects.all()
    category = None
    subcategory = None

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        product = Product.objects.filter(category=category)
    elif subcategory_slug:
        subcategory = get_object_or_404(Subcategory, slug=subcategory_slug)
        product = Product.objects.filter(category__subcategory=subcategory)
        
    context = {
        'products': product,
        'category': category,
        'subcategory': subcategory,
        'categories': categories,
    }
    return render(request, "web/shop.html", context)

# class ShopDetailView(DetailView):
#     model = Product
#     template_name = "web/shop-detail.html"
#     context_object_name = 'product'
#     slug_field = 'slug'
#     slug_url_kwarg = 'slug'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # Add cart_count to the context
#         context['request'] = self.request
#         return context
    
    
class ShopDetailView(DetailView):
    model = Product
    template_name = "web/shop-detail.html"
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        
        related_products = Product.objects.filter(subcategory=product.subcategory).exclude(id=product.id)[:6]
        
        # Add cart_count to the context
        context['request'] = self.request
        context['related_products'] = related_products
        return context
    
    