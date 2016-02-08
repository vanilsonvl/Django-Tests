# coding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.

class CustomUserManager(BaseUserManager):
     
    def create_user(self, name, email, password=None):
	
	if not email:
	    raise ValueError('Users must have an email address')

	user = self.model(email=self.normalize_email(email))
	user.name = name
	user.set_password(password)
	user.save()
	return user

    def create_superuser(self, name, email, password):

	user = self.create_user(name, email, password)
	user.is_admin = True
	user.is_staff = True
	user.save()
	return user


class CustomUser(AbstractBaseUser):
   
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
	return self.name

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
	return True

  
