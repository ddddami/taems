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


class SubjectGroup(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title


class Subject(models.Model):
    title = models.CharField(max_length=255)
    group = models.ForeignKey(SubjectGroup, on_delete=models.PROTECT)

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
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

    class Meta:
        unique_together = [['_class', 'class_arm']]


class TestType(models.Model):
    TEST_TYPE_CHOICES = [
        ('CA', 'Continuous Assessment'),
        ('EX', 'Examination'),
    ]
    title = models.CharField(max_length=255, choices=TEST_TYPE_CHOICES)

    def __str__(self) -> str:
        return self.title


class Score(models.Model):
    value = models.PositiveSmallIntegerField()
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    type = models.OneToOneField(TestType, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return str(self.value)
