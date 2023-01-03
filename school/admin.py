from datetime import datetime
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


class AgeFilter(admin.SimpleListFilter):
    title = 'age'
    parameter_name = 'birth_date'

    def lookups(self, request, model_admin):
        now = datetime.now().year
        MIN_AGE = 10
        MAX_AGE = 18
        YEARS = tuple(range(now-MAX_AGE+1, now-MIN_AGE))
        list_values_verbose = []
        [list_values_verbose.append((year, now-year)) for year in YEARS]
        return list_values_verbose

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(birth_date__gte=self.value()+'-01-01',
                                   birth_date__lt=str(int(self.value())+1)+'-01-01')
        return queryset


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name',
                    'birth_date', 'department', 'student_class')
    list_filter = ['_class', 'class_arm',
                   'department', 'subjects', AgeFilter]
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
    def students(self, subject):
        return get_students(model=subject)

    def get_queryset(self, request):
        return get_students_count(queryset=super().get_queryset(request))
