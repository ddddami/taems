from django.contrib import admin
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from .models import Student, Class, ClassArm, Department, Subject
# Register your models here.


def get_students(model):
    url = (
        reverse('admin:school_student_changelist')
        + '?'
        + urlencode({
            str(model) + '__id': str(model.id)
        }))

    return format_html('<a href="{}">{} Students</a>', url, model.students_count)


def get_students_count(queryset):
    return queryset.annotate(students_count=Count('student'))


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name',
                    'birth_date', 'department', 'student_class')
    list_filter = ['_class', 'class_arm', 'department', 'subjects']
    # list_editable = ['birth_date', 'department']
    list_select_related = ['department', '_class', 'class_arm']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    ordering = ['id']

    def student_class(self, student):
        return f'{student._class} {student.class_arm}'


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'students')
    # list_select_related = ['Student']

    @admin.display(ordering='students_count')
    def students(self, department):
        return get_students(model=department)

    def get_queryset(self, request):
        return get_students_count(queryset=super().get_queryset(request))


@admin.register(ClassArm)
class ClassArmAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'students')
    # list_select_related = ['Student']

    @admin.display(ordering='students_count')
    def students(self, class_arm):
        return get_students(model=class_arm)

    def get_queryset(self, request):
        return get_students_count(queryset=super().get_queryset(request))


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'students')
    # list_select_related = ['Student']

    @admin.display(ordering='students_count')
    def students(self, department):
        return get_students(model=department)

    def get_queryset(self, request):
        return get_students_count(queryset=super().get_queryset(request))


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'students')
    list_filter = ['group']
    # list_select_related = ['Student']

    @admin.display(ordering='students_count')
    def students(self, department):
        return get_students(model=department)

    def get_queryset(self, request):
        return get_students_count(queryset=super().get_queryset(request))
