from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
