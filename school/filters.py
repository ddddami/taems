from django_filters import rest_framework as filters
from .models import Student, Teacher


class StudentFilter(filters.FilterSet):
    class Meta:
        model = Student
        fields = {
            '_class_id': ['exact'],
            'class_arm_id': ['exact'],
            'department_id': ['exact'],
            'sex': ['exact'],
            'subjects': ['exact'],
        }


class TeacherFilter(filters.FilterSet):
    class Meta:
        model = Teacher
        fields = {
            'managed_class_id': ['exact'],
            'managed_class_arm_id': ['exact'],
            'sex': ['exact'],
            'subject': ['exact'],
        }
