from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
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


class AddressManager(models.Manager):
    def get_address_for(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)
        return Address.objects.filter(content_type=content_type, object_id=obj_id)


class Address(models.Model):
    objects = AddressManager()
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    lga = models.ForeignKey(LGA, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(unique=True)
    content_object = GenericForeignKey()

    class Meta:
        verbose_name_plural = 'Addresses'

    def __str__(self) -> str:
        return self.street + ' ' + self.city
