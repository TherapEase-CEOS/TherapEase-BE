from django.db import models

class User(models.Model):
    role = models.CharField(max_length=50)
    accountId = models.CharField(max_length=100)
    name = models.CharField(max_length=10)
    code = models.CharField(max_length=100)

class Counselor(models.Model):
    counselor = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.EmailField(max_length=30)
    introduction = models.CharField(max_length=200)
    engagement = models.CharField(max_length=150)