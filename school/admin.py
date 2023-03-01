from datetime import datetime
from django.contrib import admin
from django.db.models.aggregates import Count
from django.db.models import F
from django.utils.html import format_html, urlencode
from django.urls import reverse
from .models import AttendanceMark, Score, Session, Student, Class, ClassArm, Department, Subject, SubjectGroup, Teacher, Term, Week
# Register your models here.


def get_thumbnail(instance):
    if instance.image:
        return format_html(f'<img src="{instance.image.url}" class="thumbnail" />')
    return ''


def get_students(model_name, model):
    url = (
        reverse('admin:school_student_changelist')
        + '?'
        + urlencode({
            model_name + '__id': str(model.id)
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
        YEARS = tuple(range(now-MAX_AGE, now-MIN_AGE+1))
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
                    'birth_date', 'department', 'student_class', 'thumbnail')
    list_filter = ['_class', 'class_arm',
                   'department', 'subjects', AgeFilter]
    # list_editable = ['birth_date', 'department']
    list_select_related = ['department', '_class', 'class_arm', 'user']
    search_fields = ['user__first_name__istartswith',
                     'user__last_name__istartswith']
    ordering = ['id']
    readonly_fields = ['thumbnail']

    def thumbnail(self, instance):
        get_thumbnail(instance)

    def student_class(self, student):
        return f'{student._class} {student.class_arm}'

    class Media:
        css = {'all': ['school/styles.css']}


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'students')
    # list_select_related = ['Student']

    @admin.display(ordering='students_count')
    def students(self, _class):
        return get_students('_class', _class)

    def get_queryset(self, request):
        return get_students_count(queryset=super().get_queryset(request))


@admin.register(ClassArm)
class ClassArmAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'students')
    # list_select_related = ['Student']

    @admin.display(ordering='students_count')
    def students(self, class_arm):
        return get_students('class_arm', class_arm)

    def get_queryset(self, request):
        return get_students_count(queryset=super().get_queryset(request))


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'students')
    # list_select_related = ['Student']

    @admin.display(ordering='students_count')
    def students(self, department):
        return get_students('department', department)

    def get_queryset(self, request):
        return get_students_count(queryset=super().get_queryset(request))


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'students')
    list_filter = ['group']
    # list_select_related = ['Student']

    @admin.display(ordering='students_count')
    def students(self, subject):
        return get_students('subjects', subject)

    def get_queryset(self, request):
        return get_students_count(queryset=super().get_queryset(request))


@admin.register(SubjectGroup)
class SubjectGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'subjects')

    @admin.display(ordering='students_count')
    def subjects(self, subject_group):
        url = (
            reverse('admin:school_subject_changelist')
            + '?'
            + urlencode({
                'group__id': str(subject_group.id)
            }))

        return format_html('<a href="{}">{} Subjects</a>', url, subject_group.subjects_count)

    def get_queryset(self, request):

        return super().get_queryset(request).annotate(subjects_count=Count('subject'))


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name',
                    'birth_date', 'subject', 'thumbnail')
    list_filter = ['managed_class', 'managed_class_arm']
    list_select_related = ['user', 'subject']
    search_fields = ['user__first_name__istartswith',
                     'user__last_name__istartswith']

    class Media:
        css = {'all': ['school/styles.css']}

    def thumbnail(self, instance):
        get_thumbnail(instance)


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'value', 'student',
                    'teacher', 'date_created')
    # list_filter = ['type', 'student', 'teacher', 'teacher__subject']
    list_filter = ['type',  'teacher__subject']
    search_fields = [
        'student__user__first_name__istartswith',
        'student__user__last_name__istartswith',
        'teacher__user__first_name__istartswith',
        'teacher__user__last_name__istartswith']

    def subject(self, score):
        return Subject.objects.only('title').get(id=score.subject)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('teacher__user', 'student__user').annotate(subject=F('teacher__subject'))


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'terms')

    def terms(self, session):
        url = (
            reverse('admin:school_term_changelist')
            + '?'
            + urlencode({
                'session__id': str(session.id)
            }))

        return format_html('<a href="{}">{} Terms</a>', url, session.terms)

    def get_queryset(self, request):

        return super().get_queryset(request).annotate(terms=Count('term'))


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'start_date', 'end_date', 'session')
    list_filter = ['session', 'title']


@admin.register(Week)
class WeekAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'start_date')
    list_filter = ['start_date', 'title']


class StudentFilter(admin.SimpleListFilter):
    title = 'student'
    parameter_name = 'student'

    def lookups(self, request, model_admin):
        students = Student.objects.select_related('user').all()
        return [(student.id, f'{student.user.first_name} {student.user.last_name}') for student in students]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(student__id=self.value())


@admin.register(AttendanceMark)
class AttendanceMarkAdmin(admin.ModelAdmin):
    list_display = ('id', 'present', 'student', 'class_teacher', 'day', 'week')
    list_filter = ['present', 'day', 'week', StudentFilter]

    list_select_related = ['day', 'week', 'student', 'student__user']
