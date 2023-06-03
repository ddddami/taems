from django.db import models

# Create your models here.


class State(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class LGA(models.Model):
    name = models.CharField(max_length=255)
    state = models.ForeignKey(State, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.name
