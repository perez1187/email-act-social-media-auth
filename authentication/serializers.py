import email
from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, attrs):
        email = attrs.get('email','')

        # here we can create some validation, for example:
        # if not email.isalnum():
        #     raise serializers.ValidationError('the user should only contain alphanumeric')

        return attrs # so after validation we return attribuits
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)