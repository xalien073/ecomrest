from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import UserProfile

class UserProfileSer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'profile_image']

class SignUpSer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password', 'confirm_password', 'profile_image']

    def create(self, validated_data):
        return UserProfile.objects.create_user(**validated_data)    
