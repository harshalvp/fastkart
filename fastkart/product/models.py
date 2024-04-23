from django.db import models
from django.urls import reverse, reverse_lazy
from django.core.validators import MaxValueValidator
from colorfield.fields import ColorField
from ckeditor.fields import RichTextField
from django.utils.text import slugify

# Create your models here.
class Color(models.Model):
    name=models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    code_color = ColorField(default="FF0000")
         
    class Meta:
        verbose_name = ("Color")
        verbose_name_plural = ("Colors")
        ordering = ("name",)

    def __str__(self):
        return self.name
    

class Sale(models.Model):
    name=models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    code_color = ColorField(default="#FF0000")
         
    class Meta:
        verbose_name = ("Sale")
        verbose_name_plural = ("Sales")
        ordering = ("name",)

    def __str__(self):
        return self.name
    
class  Brand(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    slug = models.CharField(max_length=200)
    
    class Meta:
        verbose_name = ("Brand")
        verbose_name_plural = ("Brands")

    def __str__(self):
        return self.name
    

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    class Meta:
        verbose_name = ('Category')
        verbose_name_plural = ('Categorys')

    def __str__(self):
        return f"{self.name}"
    
    def product_count(self):
        return Product.objects.filter(category=self).count()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    is_combo = models.BooleanField(default=False)

    class Meta:
        verbose_name = ('Subcategory')
        verbose_name_plural = ('Subcategories')

    def __str__(self):
        return f"{self.name}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('subcategory_detail', kwargs={'slug': self.slug})
    
         
class Approve(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    is_approve = models.BooleanField(default=False)

    class Meta:
        verbose_name = ('Approve')
        verbose_name_plural = ('Approves')
        
    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name="subcategory")
    approve = models.ForeignKey(Approve, on_delete=models.CASCADE, related_name="approve")
    name = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500)
    image = models.ImageField(upload_to='media/products')
    rating = models.PositiveIntegerField(
        validators=[MaxValueValidator(5)],
        default=5,
        verbose_name="Product Rating(max:5)",
    )
    product_information = RichTextField(blank=True, null=True)
    description = RichTextField(blank=True, null=True)
    background_color = models.ForeignKey(Sale,on_delete=models.CASCADE, blank=True, null=True)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE, blank=True, null=True)
    new_arrival = models.BooleanField(default=False)
    best_sell = models.BooleanField(default=False)
    feature = models.BooleanField(default=False)
    special_offer = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_stock = models.BooleanField(default=True)
    is_approve = models.BooleanField(default=True)
    
    class Meta:
        ordering = [
            "id",
        ]
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name
    
    def get_images(self):
        return Product_Image.objects.filter(image_product=self)
    
    def related_products(self):
        return Product.objects.filter().exclude(pk=self.pk).distinct()[0:12]
    
    def get_absolute_url(self):
        return reverse("product:shop-detail", kwargs={"slug": self.slug})
    
    
    def get_additional(self):
        return Additional_Information.objects.filter(additional_product=self)
    
    def get_company(self):
        return Company.objects.filter(additional_product=self)
    
    def get_sizes(self):
        return AvailableSize.objects.filter(color_product=self)
    
    # def get_sizestwo(self):
    #     return AvailableSizetwo.objects.filter(color_product=self)
    
    def get_sale_price(self):
        return min([p.sale_price for p in self.get_sizes()])

    def get_regular_price(self):
        sizes = self.get_sizes()
        valid_prices = [p.regular_price for p in sizes if p.regular_price is not None]
        return min(valid_prices) if valid_prices else None
    

class AvailableSize(models.Model):
    SIZE_CHOICES = (
        ("S", "Small"),
        ("M", "Medium"),
        ("L", "Large"),
        ("XL", "Extra Large"),
        ("2XL", "2XL"),
        ("3XL", "3XL"),
        ("4XL", "4XL"),
        ("NA", "NA"),
    )
    color_product = models.ForeignKey(Product,on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    size_category = models.CharField(max_length=10, choices=SIZE_CHOICES,default="S")
    sale_price = models.FloatField(blank=True, null=True)
    regular_price = models.FloatField(blank=True,null=True)
    thickness = models.CharField(max_length=100, blank=True, null=True)
    size = models.CharField(max_length=100, blank=True, null=True,) 
    work_file = models.FileField(upload_to="media/work_files/", blank=True, null=True) 
    regular_price_approved = models.BooleanField(default=False)
       

    class Meta:
        verbose_name = ("Available Size")
        verbose_name_plural = ("Available Sizes")

    def offer_percent(self):
        if self.regular_price and self.regular_price != self.sale_price:
            return ((self.regular_price - self.sale_price) / self.regular_price) * 100
        return 0

    def __str__(self):
        return str(self.name)


# class AvailableSizetwo(models.Model):
#     SIZE_CHOICES = (
#         ("S", "Small"),
#         ("M", "Medium"),
#         ("L", "Large"),
#         ("XL", "Extra Large"),
#         ("2XL", "2XL"),
#         ("3XL", "3XL"),
#         ("4XL", "4XL"),
#         ("NA", "NA"),
#     )
#     color_product = models.ForeignKey(Product,on_delete=models.CASCADE)
#     name = models.CharField(max_length=200, null=True, blank=True)
#     size_category = models.CharField(max_length=10, choices=SIZE_CHOICES,default="S")
#     sale_price = models.FloatField(blank=True,null=True)
#     thickness = models.CharField(max_length=100, blank=True, null=True)
#     size = models.CharField(max_length=100, blank=True, null=True,) 
#     work_file = models.FileField(upload_to="media/work_files/", blank=True, null=True)         

#     class Meta:
#         verbose_name = ("Available Size no offer")
#         verbose_name_plural = ("Available Sizes")
    
#     def offer_percent(self):
#         if self.regular_price and self.regular_price != self.sale_price:
#             return ((self.regular_price - self.sale_price) / self.regular_price) * 100   

#     def __str__(self):
#         return str(self.name)


class Product_Image(models.Model):
    image_product = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = models.ImageField(upload_to = "media/product_image/")

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
        ordering = "image_product",


class Additional_Information(models.Model):
    additional_product = models.ForeignKey(Product,on_delete=models.CASCADE)
    specification = models.CharField(max_length=500)
    detail = models.CharField(max_length=500)

    class Meta:
        verbose_name = "additional information"
        verbose_name_plural = "additional informations"

class Company(models.Model):
    additional_product = models.ForeignKey(Product,on_delete=models.CASCADE)
    specification = models.CharField(max_length=500)
    detail = models.CharField(max_length=500)

    class Meta:
        verbose_name = "company"
        verbose_name_plural = "companys"