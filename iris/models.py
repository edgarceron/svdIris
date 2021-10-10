from django.db import models
from django.contrib.postgres.fields import ArrayField
from numpy import empty

# Create your models here.
class Irises(models.Model):
    """"Modelo para los usuarios del sistema"""
    name = models.CharField(max_length=50)
    lef = ArrayField(ArrayField(models.IntegerField()))
    right = ArrayField(ArrayField(models.IntegerField()))
