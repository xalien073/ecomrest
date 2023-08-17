from rest_framework import serializers
from .models import Cart

class CartSer(serializers.ModelSerializer):
    Product_Name = serializers.CharField(source='Product.product_name', read_only=True)
    Price = serializers.IntegerField(source='Product.price', read_only=True)
    Slug = serializers.SlugField(source='Product.slug', read_only=True)
    Image = serializers.ImageField(source='Product.image', read_only=True)
    class Meta:
        model = Cart
        fields = ['id', 'Customer', 'Product', 'Product_Name', 'Qty',
                'Price', 'ProductSubtotal', 'Slug', 'Image']
