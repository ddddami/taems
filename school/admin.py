from django.contrib import admin
from .models import Student, Class, ClassArm, Department, Subject
# Register your models here.


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'birth_date', )
    list_select_related = ['subject', 'department', '_class', 'class_arm']


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    # list_select_related = ['Student']


@admin.register(ClassArm)
class ClassArmAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    # list_select_related = ['Student']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    # list_select_related = ['Student']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    # list_select_related = ['Student']
