from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.decorators import action
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import status
from .serializers import AddScoreSerializer, AttendanceMarkSerializer, ScoreSerializer, StudentSerializer, AddStudentSerializer, SubjectSerializer, TeacherSerializer, AddTeacherSerializer
from .models import AttendanceMark, Score, ScoreSheet, Student, Subject, Teacher
from .permissions import FullDjangoModelPermission
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
    permission_classes = [FullDjangoModelPermission]

    def get_queryset(self):
        user_id = self.request.user.id
        school_id = Teacher.objects.get(user_id=user_id).school.id
        return Student.objects.select_related(
            'user', '_class', 'class_arm', 'department', 'school').filter(school_id=school_id)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return AddStudentSerializer
        return StudentSerializer

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        student = Student.objects.get(
            user_id=request.user.id)
        if request.method == 'GET':
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = AddStudentSerializer(student, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class TeacherViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TeacherFilter
    pagination_class = DefaultPagination
    search_fields = ['^user__first_name',
                     '^user__last_name', '^user__middle_name']
    ordering_fields = ['id']
    permission_classes = [FullDjangoModelPermission]

    queryset = Teacher.objects.select_related(
        'user', 'managed_class', 'managed_class_arm', 'subject').all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return AddTeacherSerializer
        return TeacherSerializer

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        teacher = Teacher.objects.get(
            user_id=request.user.id)
        if request.method == 'GET':
            serializer = TeacherSerializer(teacher)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = AddTeacherSerializer(teacher, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class ScoreViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]
    serializer_class = ScoreSerializer

    def get_serializer_context(self):
        user = self.request.user
        if Teacher.objects.filter(user_id=user.id).exists():
            return {'teacher_id': user.teacher.id}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddScoreSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        user = self.request.user
        queryset = Score.objects.select_related(
            'type', 'scoresheet').all()
        session_id = self.request.query_params.get('session_id')
        term_id = self.request.query_params.get('term_id')
        subject_id = self.request.query_params.get('subject_id')
        school_id = self.request.query_params.get('school_id')
        class_id = self.request.query_params.get('class_id')
        class_arm_id = self.request.query_params.get('class_arm_id')
        if user.is_staff:
            teacher_id = Teacher.objects.only('id').filter(
                school_id=school_id, subject_id=subject_id, _class_id=class_id, class_arm_id=class_arm_id).first()
            scoresheet_id = ScoreSheet.objects.only('id').filter(
                session_id=session_id, term_id=term_id, teacher_id=teacher_id).first()
            return queryset.filter(scoresheet_id=scoresheet_id)
        if Teacher.objects.filter(user_id=user.id).exists():
            teacher_id = Teacher.objects.only('id').get(user_id=user.id)
            scoresheet_id = ScoreSheet.objects.only('id').filter(
                teacher_id=teacher_id, session_id=session_id, term_id=term_id, _class_id=class_id, class_arm_id=class_arm_id).first()
            return queryset.select_related('student__user').filter(scoresheet_id=scoresheet_id)
        student = Student.objects.get(user_id=user.id)
        # print(session_id) I dont know why it's printing 4 times ...yet
        return queryset.filter(session_id=session_id, term_id=term_id, student_id=student.id)

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
            if serializer.is_valid():
                # for score in serializer.validated_data:
                # score['teacher_id'] = request.user.teacher.id
                # score['scoresheet_id'] = scoresheet.id
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                # serializer.save(teacher_id=request.user.teacher.id)
                # serializer.save(scoresheet_id=scoresheet.id)
                serializer.save()
                return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AttendanceMarkViewSet(ModelViewSet):
    permission_classes = [DjangoModelPermissions]

    queryset = AttendanceMark.objects.select_related(
        'student__user', 'class_teacher__user').all()
    serializer_class = AttendanceMarkSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}


class SubjectViewSet(ListModelMixin, GenericViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
