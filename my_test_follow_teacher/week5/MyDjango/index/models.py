from django.db import models


# Create your models here.

class Type(models.Model):
    # id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=20)


class Name(models.Model):
    # id auto
    name = models.CharField(max_length=80)
    author = models.CharField(max_length=30)
    stars = models.CharField(max_length=15)
