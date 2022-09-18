import email
from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from .models import User

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