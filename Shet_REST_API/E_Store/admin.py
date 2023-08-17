from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import Category, Brand, Product, Contact, StarRating

admin.site.register((Category, Brand, Product, Contact, StarRating, ))
