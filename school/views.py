from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import StudentSerializer, AddStudentSerializer, TeacherSerializer, AddTeacherSerializer
from .models import Student, Teacher
from .filters import StudentFilter, TeacherFilter
from .paginator import DefaultPagination

# Create your views here.


class StudentViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = StudentFilter
    pagination_class = DefaultPagination
    search_fields = ['^user__first_name',
                     '^user__last_name', '^user__middle_name']
    ordering_fields = ['id']

    def get_queryset(self):
        return Student.objects.select_related(
            'user', '_class', 'class_arm', 'department').all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return AddStudentSerializer
        return StudentSerializer


class TeacherViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TeacherFilter
    search_fields = ['^user__first_name',
                     '^user__last_name', '^user__middle_name']
    ordering_fields = ['id']
    queryset = Teacher.objects.select_related(
        'user', '_class', 'class_arm', 'subject').all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return AddTeacherSerializer
        return TeacherSerializer
