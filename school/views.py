from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import AddScoreSerializer, AttendanceMarkSerializer, ScoreSerializer, StudentSerializer, AddStudentSerializer, TeacherSerializer, AddTeacherSerializer
from .models import AttendanceMark, Score, Student, Teacher
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
    permission_classes = [DjangoModelPermissions]

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
    pagination_class = DefaultPagination
    search_fields = ['^user__first_name',
                     '^user__last_name', '^user__middle_name']
    ordering_fields = ['id']
    permission_classes = [DjangoModelPermissions]

    queryset = Teacher.objects.select_related(
        'user', 'managed_class', 'managed_class_arm', 'subject').all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return AddTeacherSerializer
        return TeacherSerializer


class ScoreViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]

    # TODO: Work on massive upload
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return AddScoreSerializer
        return ScoreSerializer

    def get_serializer_context(self):
        return self.request.user.teacher.id

    def get_queryset(self):
        user = self.request.user
        queryset = Score.objects.select_related(
            'teacher__user', 'student__user', 'type', 'term', 'session').all()
        if user.is_staff:
            return queryset
        if Teacher.objects.filter(user_id=user.id).exists():
            teacher_id = Teacher.objects.only('id').get(user_id=user.id)
            return queryset.filter(teacher_id=teacher_id)
        student_id = Student.objects.only('id').get(user_id=user.id)
        return queryset.filter(student_id=student_id)


class AttendanceMarkViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]

    queryset = AttendanceMark.objects.select_related(
        'student__user', 'class_teacher__user').all()
    serializer_class = AttendanceMarkSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}
