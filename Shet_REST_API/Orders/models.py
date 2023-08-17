from django.db import models
from django.utils.timezone import now
from UserProfile .models import UserProfile
from E_Store .models import Product
# Create your models here.
class Shipping_Address(models.Model):
    User = models.ForeignKey(UserProfile, on_delete=models.CASCADE)    
    Name = models.CharField(max_length=50)
    Email = models.EmailField()
    Address = models.TextField()
    City = models.CharField(max_length=20)
    State = models.CharField(max_length=20)
    Zip_Code = models.CharField(max_length=10)
    Phone = models.CharField(max_length=12, default="")
    Secondary_Phone = models.CharField(max_length=12, default="", blank=True)

    def __str__(self):
        return self.Address +', '+ self.City +'-'+ self.Zip_Code +', '+ self.State

class ProductOrdered(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.PROTECT)
    Qty = models.IntegerField()
    ProductSubtotal = models.IntegerField()#DecimalField(max_digits=30, decimal_places=2)
    
    def __str__(self):
        return '%i' % (self.id)

class Order(models.Model):
    Placed = 'Placed'
    OnTheWay = 'On the way'
    Delivered = 'Delivered'

    STATUS_CHOICES = (
        (Placed, 'Placed'),
        (OnTheWay, 'On the way'),
        (Delivered, 'Delivered')
    )
    Order_Id = models.AutoField(primary_key=True)
    Created = models.DateTimeField(default=now)
    Customer = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    Orders = models.ManyToManyField(ProductOrdered,
    related_name='order', verbose_name='Product')
    Address = models.ForeignKey(Shipping_Address, on_delete=models.PROTECT)
    Subtotal = models.DecimalField(max_digits=30, decimal_places=2)
    Status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=Placed)

    def __str__(self):
        return "%i for %s Subtotal= Rs.%d" %(self.Order_Id, self.Customer.email, self.Subtotal)

# class OrderUpdate(models.Model):
#     update_id = models.AutoField(primary_key=True)
#     order_id = models.IntegerField(default="")
#     update_desc = models.CharField(max_length=5000)
#     timestamp = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return self.update_desc[0:7] + "..."
