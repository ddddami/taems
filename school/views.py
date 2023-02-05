from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import StudentSerializer, AddStudentSerializer
from .models import Student

# Create your views here.


class StudentList(ListCreateAPIView):

    def get_queryset(self):
        return Student.objects.select_related(
            'user', '_class', 'class_arm').all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddStudentSerializer
        return StudentSerializer


class StudentDetail(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return AddStudentSerializer
        return StudentSerializer
