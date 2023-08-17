from rest_framework import serializers
from .models import Shipping_Address, Order, ProductOrdered

class ShippingAddressSer(serializers.ModelSerializer):
   class Meta:
        model =  Shipping_Address
        fields = "__all__"

class ProductOrderedSer(serializers.ModelSerializer):
  Image = serializers.ImageField(source='Product.image', read_only=True)
  class Meta:
      model = ProductOrdered
      fields = ['id', 'Product', 'Qty', 'ProductSubtotal', 'Image']

class OrderSer(serializers.ModelSerializer):
  class Meta:
        model =  Order
        fields = ['Order_Id', 'Customer', 'Address', 'Orders', 'Subtotal', 'Status']
        
class GetOrderSer(serializers.ModelSerializer):
  class Meta:
        model =  Order
        fields = ['Status', 'Created', 'Order_Id', 'Orders', 'Subtotal']
        depth = 2