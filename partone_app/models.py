from django.db import models
from .base.models import BaseModel
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    is_email_verified = models.BooleanField(default=False)
    location = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return "Profile: " + self.user.username


class Category(BaseModel):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return "Category: " + self.name
    
class Product(BaseModel):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    product_description = models.TextField()
    
    def __str__(self):
        return "ProductName: " + self.name
    

class ProductPrice(BaseModel):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.0, max_digits=7, null= True, blank = True, decimal_places=2)
    
    def __str__(self):
        return "ProductPrice: " + self.product.name
    
    

class ProductInventory(BaseModel):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    stock_quantity = models.PositiveIntegerField(default=0, null = True, blank=True)
    
    def __str__(self):
        return "ProductInventory: " + self.product.name
    
    
class CartItem(BaseModel):
    customer = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, null=True,blank=True,on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(default=0)
    def __str__(self):
        return "CartItem: " + str(self.id)


class Cart(BaseModel):
    customer = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    total_price = models.DecimalField(default=0.0, max_digits=7, null= True, blank = True, decimal_places=2)

    def __str__(self):
        return "Cart: " + str(self.id)