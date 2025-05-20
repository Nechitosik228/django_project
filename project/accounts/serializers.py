from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'



class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'


class RegisterFormSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    captcha = serializers.CharField()

    class Meta:
        model = User
        extra_fields = ['email']
        fields = ['username', 'password1', 'password2']
