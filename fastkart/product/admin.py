from django.contrib import admin
from .models import (
    Category,
    Product,
    Color,
    AvailableSize,
    Sale,
    Brand,
    Product_Image,
    Additional_Information,
    Subcategory,
    Company,
    Approve,
)

# Register your models here.
class AvailableSizeInline(admin.TabularInline):
    model = AvailableSize
    extra = 0

# class AvailableSizetwoInline(admin.TabularInline):
#     model = AvailableSizetwo
#     extra = 0

class Product_ImageInline(admin.TabularInline):
    model = Product_Image
    extra = 0

class Additional_InformationInline(admin.TabularInline):
    model = Additional_Information
    extra = 0
    
class CompanyInline(admin.TabularInline):
    model = Company
    extra = 0

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name','slug','code_color',)  
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Subcategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['category']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug','image','category')
    prepopulated_fields = {"slug": ("name",)}
    inlines = [AvailableSizeInline, Product_ImageInline, Additional_InformationInline,CompanyInline]


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('name','slug',)
    prepopulated_fields ={'slug': ('name',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name','slug',)
    prepopulated_fields ={'slug': ('name',)}
    
    
@admin.register(Approve)
class ApproveAdmin(admin.ModelAdmin):
    list_display = ('name','slug', 'is_approve',)
    prepopulated_fields ={'slug': ('name',)}
        
    
    
    
class AvailableSizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'size_category', 'sale_price', 'regular_price', 'offer_percent']
    search_fields = ['name', 'size_category']

    # def get_fields(self, request, obj=None):
    #     fields = super().get_fields(request, obj)
    #     if obj and obj.approval_status != 'approved':
    #         fields.remove('regular_price')  # Remove regular_price field if approval status is not approved
    #     return fields