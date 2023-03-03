from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from autoslug import AutoSlugField

class UserProfile(models.Model):
    user = models.CharField(max_length=100, primary_key=True)


    def __str__(self):
        return self.user.username

class Movies(models.Model):
    movieName = models.CharField(max_length=100)