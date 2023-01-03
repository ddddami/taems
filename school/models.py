from django.db import models

# Create your models here.


class Class(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Classes'

    def __str__(self) -> str:
        return self.title


class ClassArm(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title


class Department(models.Model):
    DEPARTMENT_CHOICES = [
        ('Bu', 'Business'),
        ('Hu', 'Hummanities'),
        ('Sc', 'Science'),
    ]
    title = models.CharField(max_length=255, choices=DEPARTMENT_CHOICES)

    def __str__(self) -> str:
        return self.title


class Teacher(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    taught_classes = models.ManyToManyField(Class)
    taught_arms = models.ManyToManyField(ClassArm)
    _class = models.ForeignKey(
        Class, on_delete=models.SET_NULL, related_name='class_teacher_set', null=True)
    class_arm = models.ForeignKey(
        ClassArm, on_delete=models.SET_NULL, related_name='class_teacher_set', null=True)


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
    teacher = models.OneToOneField(Teacher, models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.title


class Student(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    _class = models.ForeignKey(Class, on_delete=models.PROTECT)
    class_arm = models.ForeignKey(ClassArm, on_delete=models.PROTECT)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    subjects = models.ManyToManyField(Subject)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
