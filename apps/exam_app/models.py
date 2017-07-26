from __future__ import unicode_literals

from django.db import models
import time

# Create your models here.

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 4 or len(postData['username']) < 4:
            errors['name'] = "Name and username must be at least 3 characters"
        if len(postData['password']) < 9:
            errors['password'] = "Password should be at least 8 characters"
        if postData['password'] != postData['confirm_pw']:
            errors['password'] = "Passwords do not match"
        if postData['date'] == '':
            errors['date'] = "Date Hire required"
        print postData['date']
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    date_hired = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Wishlist(models.Model):
    item = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, related_name='wishlists')
    wishlists = models.ManyToManyField(User, related_name="m2m_wishlists")
