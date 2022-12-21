from django.db import models

# Create your models here.
class Class(models.Model):
    title = models.CharField(max_length=255)


class ClassArm(models.Model):
    title = models.CharField(max_length=255)


class Department(models.Model):
    DEPARTMENT_CHOICES = [
        ('Bu', 'Business'),
        ('Hu', 'Hummanities'),
        ('Sc', 'Science'),
    ]
    title = models.CharField(max_length=255, choices=DEPARTMENT_CHOICES)

class Subject(models.Model):
    SUBJECT_GROUP_CHOICES = [
        ('Bu', 'Business'),
        ('Ge', 'General'),
        ('Hu', 'Hummanities'),
        ('Sc', 'Science'),
        ('Tr', 'Trade')
    ]
    title = models.CharField(max_length=255)
    group = models.CharField(max_length=255, choices=SUBJECT_GROUP_CHOICES)


class Student(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    _class = models.ForeignKey(Class, on_delete=models.PROTECT)
    class_arm = models.ForeignKey(ClassArm, on_delete = models.PROTECT)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
