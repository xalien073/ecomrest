from django.contrib import admin
import datetime
from django.urls import reverse
from .models import Shipping_Address, Order, ProductOrdered
# Register your models here.
def Customer(obj):
    return '%s %s' % (obj.Customer.first_name, obj.Customer.last_name)
Customer.short_description = 'Customer Name'

def Subtotal(obj):
    return '%s %i' % ('Rs', obj.Subtotal)
Subtotal.short_description = 'Subtotal'

def OrderOnTheWay(modeladmin, request, queryset):
    for order in queryset:
        order.Status = Order.OnTheWay
        order.save()
    return
OrderOnTheWay.short_description = 'Set as On the way!'

def OrderDelivered(modeladmin, request, queryset):
    for order in queryset:
        order.Status = Order.Delivered
        order.save()
    return
OrderDelivered.short_description = 'Set as Delivered'

class ProductOrderedInline(admin.TabularInline):
    model = Order.Orders.through
    fields = ['productordered','Product', 'Qty', 'ProductSubtotal']
    readonly_fields = ['Product', 'Qty','ProductSubtotal']
    can_delete = False
    verbose_name = 'Product'
    verbose_name_plural = 'Products'
    extra = 0

    def Product(self, instance):
        return instance.productordered.Product
    Product.short_description = 'Product'    
    
    def Qty(self, instance):
        return instance.productordered.Qty
    Qty.short_description = 'Qty'    

    def ProductSubtotal(self, instance):
        return instance.productordered.ProductSubtotal
    ProductSubtotal.short_description = 'Product Subtotal'

class OrderAdmin(admin.ModelAdmin):
    list_display = ['Order_Id', Customer, Subtotal, 'Status']
    list_filter = ['Created', 'Status']
    search_fields = ['Status']
    exclude = ['Orders']
    inlines = [ProductOrderedInline]
    actions = [OrderOnTheWay, OrderDelivered]

class ProductOrderedAdmin(admin.ModelAdmin):
    list_display = ['Product', 'Qty', 'ProductSubtotal']    

admin.site.register(Order, OrderAdmin)
admin.site.register(ProductOrdered, ProductOrderedAdmin)
admin.site.register(Shipping_Address)