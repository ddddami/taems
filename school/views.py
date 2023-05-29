from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import status
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
    serializer_class = ScoreSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddScoreSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        user = self.request.user
        queryset = Score.objects.select_related(
            'type', 'term', 'session').all()
        if user.is_staff:
            return queryset
        if Teacher.objects.filter(user_id=user.id).exists():
            teacher_id = Teacher.objects.only('id').get(user_id=user.id)
            return queryset.select_related('teacher__user', 'student__user').filter(teacher_id=teacher_id)
        student_id = Student.objects.only('id').get(user_id=user.id)
        return queryset.filter(student_id=student_id)

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
            if serializer.is_valid():
                for score in serializer.validated_data:
                    score['teacher_id'] = request.user.teacher.id
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(teacher_id=request.user.teacher.id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AttendanceMarkViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]

    queryset = AttendanceMark.objects.select_related(
        'student__user', 'class_teacher__user').all()
    serializer_class = AttendanceMarkSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}
