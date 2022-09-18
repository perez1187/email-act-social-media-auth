from pyexpat import model
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from django.contrib import auth

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, attrs):
        email = attrs.get('email','')
        password = attrs.get('password','')
        pass_err_mess= {
            'eng':'password should be at least 6 characters long',
            'pl':'haslo powinno miec conajmniej 6 znaków'
            }
        if len(password)<6:
            raise serializers.ValidationError(pass_err_mess)

        return attrs # so after validation we return attribuits
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class EmailVerificationSerializer(serializers.ModelSerializer):
    token= serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['token']

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=68,write_only=True)
    tokens = serializers.CharField(max_length= 68, read_only=True)

    class Meta:
        model= User
        fields= ['email', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user=auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('invalid credentials, try again')

        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')

        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'email':user.email,
            'tokens': user.tokens
        }