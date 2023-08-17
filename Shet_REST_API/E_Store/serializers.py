from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Product, Contact, StarRating

class ProductSer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        depth = 1

class ContactSer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"

class StarRatingSer(serializers.ModelSerializer):
    class Meta:
        model = StarRating
        fields = "__all__"

class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StarRating
        fields = "__all__"
        depth = 1                                          