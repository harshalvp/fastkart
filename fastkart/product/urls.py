from django.urls import path
from . import views

app_name = "product"

# URL patterns
urlpatterns = [
    path("", views.index, name="index"),
    path("shop/", views.shop, name="shop"),
    path('shop/<slug:slug>/', views.ShopDetailView.as_view(), name="shop-detail"), 
    path('shop/category/<slug:category_slug>/', views.shop, name='category_shop'),
    path('shop/subcategory/<slug:subcategory_slug>/', views.shop, name='subcategory_shop'),
    
]