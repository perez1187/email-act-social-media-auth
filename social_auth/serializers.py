import os
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from . import google
from .register import register_social_user

from decouple import config

class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        print('user dataaaaaaaaaaa',user_data)
        print('suuuuub', user_data['sub'])
        print('auuuud', user_data['aud'])
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        #if user_data['aud'] != os.environ.get('GOOGLE_CLIENT_ID'):
        if user_data['aud'] != config('GOOGLE_TEST_ID'):

            raise AuthenticationFailed('oops, who are you?')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name)