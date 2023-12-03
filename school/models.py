from django.db import models
from django.conf import settings
from .validators import validate_file_size, validate_score_size
# Create your models here.


class School(models.Model):
    short_name = models.CharField(max_length=7)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, unique=True)
    logo = models.ImageField(null=True, blank=True,
                             default='school/images/school.png')

    def __str__(self) -> str:
        return self.name


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
    groups = models.ManyToManyField(SubjectGroup, related_name='subjects')

    def __str__(self) -> str:
        return self.title


class Student(models.Model):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    birth_date = models.DateField()
    admission_year = models.PositiveBigIntegerField(null=False)
    _class = models.ForeignKey(
        Class, on_delete=models.PROTECT, db_column='class_id')
    class_arm = models.ForeignKey(ClassArm, on_delete=models.PROTECT)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    subjects = models.ManyToManyField(Subject)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='school/images', default='school/images/user.png', null=True, validators=[validate_file_size])
    school = models.ForeignKey(School, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def middle_name(self):
        return self.user.middle_name


class Teacher(models.Model):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    birth_date = models.DateField()
    taught_classes = models.ManyToManyField(Class)
    taught_arms = models.ManyToManyField(ClassArm)
    managed_class = models.ForeignKey(
        Class, on_delete=models.SET_NULL, related_name='class_teacher_set', blank=True, null=True)
    managed_class_arm = models.ForeignKey(
        ClassArm, on_delete=models.SET_NULL, related_name='class_teacher_set', blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='school/images', default='school/images/user.png', null=True, validators=[validate_file_size])
    school = models.ForeignKey(School, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def middle_name(self):
        return self.user.middle_name

    class Meta:
        unique_together = [['managed_class', 'managed_class_arm']]


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


class ScoreSheet(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    submitted = models.BooleanField(default=False)
    session = models.ForeignKey(Session, on_delete=models.PROTECT)
    term = models.ForeignKey(Term, on_delete=models.PROTECT)
    date_created = models.DateField(auto_now_add=True)
    _class = models.ForeignKey(Class, on_delete=models.PROTECT)
    class_arm = models.ForeignKey(ClassArm, on_delete=models.PROTECT)

    class Meta:
        unique_together = [('teacher', 'term', 'session')]


class Score(models.Model):
    value = models.PositiveSmallIntegerField(validators=[validate_score_size])
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    type = models.ForeignKey(TestType, on_delete=models.PROTECT)
    last_edited = models.DateField(auto_now=True)
    scoresheet = models.ForeignKey(ScoreSheet, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.value)

    class Meta:
        unique_together = [('student', 'scoresheet', 'type')]


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
