'''
    1. we create a new User model base on Abstract User
    2. we create a new User Manager base on Base User Manager
'''

from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)

class UserManager(BaseUserManager):

    def create_user(self, email, password=None):

        # validation

        if email is None:
            raise TypeError('User should have an Email')
        
        if password is None:
            raise TypeError('Password should not be none')

        # creating user

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,email, password=None):
        if email is None:
            raise TypeError('User should have an Email')
        
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = None  # because we dont want username
    email = models.EmailField(max_length=255, unique=True, db_index=True) # db_idndex for faster search
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    USERNAME_FIELD = 'email' # we set email as login field
    REQUIRED_FIELDS = [] # we dont have other required fields

    objects = UserManager()

    def __str__(self):
        return self.email

    def token(self):
        return 'token soon model'