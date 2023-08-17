from django.db import models
from django.utils.timezone import now
from django.db.models.signals import pre_save
from django.utils.text import slugify
from UserProfile .models import UserProfile
from E_Store .models import Product
# Create your models here.
class Cart(models.Model):
    Customer = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING)
    Product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    Qty = models.IntegerField()
    ProductSubtotal = models.IntegerField()#DecimalField(max_digits=30, decimal_places=2)
   
    def __str__(self):
        return self.Product.product_name
