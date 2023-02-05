from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import StudentSerializer, AddStudentSerializer
from .models import Student

# Create your views here.


class StudentViewSet(ModelViewSet):
    def get_queryset(self):
        return Student.objects.select_related(
            'user', '_class', 'class_arm', 'department').all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return AddStudentSerializer
        return StudentSerializer
