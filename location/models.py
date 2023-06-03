from django.db import models

# Create your models here.


class State(models.Model):
    name = models.CharField(max_length=255)


class LGA(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=7, unique=True, default='Z')
    state = models.ForeignKey(State, on_delete=models.PROTECT)
