from operator import mod
from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  nickname = models.CharField(max_length=30, blank=True)


class Room(models.Model):
  owner = models.OneToOneField(Account, on_delete=models.CASCADE)
  mate = models.ForeignKey(Account)