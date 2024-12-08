from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    
    roleEnum = [('company', 'COMPANY'), ('freelancer', 'FREELANCER')]
    
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None
    role = models.CharField(max_length=200, null=False,  default=None, choices=roleEnum)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []