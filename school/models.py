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
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    birth_date = models.DateField()
    _class = models.ForeignKey(Class, on_delete=models.PROTECT)
    class_arm = models.ForeignKey(ClassArm, on_delete=models.PROTECT)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    subjects = models.ManyToManyField(Subject)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'


class Teacher(models.Model):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
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


class Session(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title


class Term(models.Model):

    TERM_CHOICES = [
        ('F', 'First Term'),
        ('S', 'Second Term'),
        ('T', 'Third term')
    ]

    title = models.CharField(max_length=1, choices=TERM_CHOICES)
    session = models.ForeignKey(Session, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField(null=True)

    def __str__(self) -> str:
        return self.title


class Score(models.Model):
    value = models.PositiveSmallIntegerField()
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    type = models.ForeignKey(TestType, on_delete=models.PROTECT)
    date_created = models.DateField(auto_now_add=True)
    last_edited = models.DateField(auto_now=True)
    session = models.ForeignKey(Session, on_delete=models.PROTECT)
    term = models.ForeignKey(Term, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return str(self.value)

    class Meta:
        unique_together = [('student', 'teacher', 'term', 'type')]


class Day(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title


class Week(models.Model):
    WEEK_CHOICES = [
        ('First', 'First Week'),
        ('Second', 'Second Week'),
        ('Third', 'Third Week'),
        ('Fourth', 'Fourth Week'),
        ('Fifth', 'Fifth Week'),
    ]
    title = models.CharField(max_length=255, choices=WEEK_CHOICES)
    start_date = models.DateField(auto_now_add=True)
    days = models.ManyToManyField(Day)

    def __str__(self) -> str:
        return self.title


class AttendanceMark(models.Model):
    present = models.BooleanField(default=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_teacher = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True)
    date_marked = models.DateField(auto_now_add=True)
    week = models.ForeignKey(Week, on_delete=models.PROTECT)
    day = models.ForeignKey(Day, on_delete=models.PROTECT)

    class Meta:
        unique_together = [('student', 'day', 'week')]

    def __str__(self) -> str:
        if self.present:
            return 'Present'
        return 'Absent'
