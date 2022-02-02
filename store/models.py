from tabnanny import verbose

from django.conf import Settings, settings
from django.db import models
from django.urls import reverse


class ProductManager(models.Manager):
    
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255,db_index=True)
    slug = models.SlugField(max_length=255,unique=True)
    
    class Meta:
        # it will show categories in the admin panel instead of category
        verbose_name_plural = 'categories'
    
    def get_absolute_url(self):
        return reverse("store:category_list",args=[self.slug])

    def __str__(self):
        return self.name
    

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product',on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='product_creator')
    title = models.CharField(max_length=255,default='admin')
    author = models.CharField(max_length=255,default='admin')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', default='images/default.png')
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=4,decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    products = ProductManager()
    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created',)
    
    def get_absolute_url(self):
        return reverse("store:product_detail",args=[self.slug])
    
    def __str__(self):
        return self.title

'''
Django Request Response Cycle

Html Request is sent 
-> URL should be matched from the urls in the project 
-> URL then is attached to a view 
-> view get data from the database 
-> data is rendered to the template 
-> template is sent back to the user
'''