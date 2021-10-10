from django.db import models
from django.contrib.postgres.fields import ArrayField
from numpy import empty

# Create your models here.
class Irises(models.Model):
    """"Modelo para los usuarios del sistema"""
    name = models.CharField(max_length=50, unique=True)
    left = ArrayField(ArrayField(models.FloatField()), blank=False)
    right = ArrayField(ArrayField(models.FloatField()), blank=False)

def nameFile(instance, filename):
    return '/'.join(['images', str(instance.name), filename])

class UploadImage(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=nameFile, blank=True, null=True)
