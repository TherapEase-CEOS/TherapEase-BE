from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('상담사', '상담사'),
        ('내담자', '내담자'),
    )

    code = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    accountId = models.CharField(max_length=100)
    name = models.CharField(max_length=10)



class Counselor(models.Model):
    # user 모델과 profile을 1:1로 연결
    counselor = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.EmailField(max_length=30)
    introduction = models.CharField(max_length=200)
    # engagement = models.CharField(max_length=150)