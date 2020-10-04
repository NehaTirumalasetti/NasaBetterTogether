from __future__ import unicode_literals
from django.db import models
from django.db import models

# Create your models here.
class Nasa(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    eventType = models.CharField(max_length=1000)
    description = models.CharField(max_length=10000)

class Authentic(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    eventType = models.CharField(max_length=1000)
    description = models.CharField(max_length=10000)
    links = models.CharField(max_length=5000)
    twitter = models.CharField(max_length=100)