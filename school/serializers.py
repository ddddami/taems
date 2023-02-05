from rest_framework import serializers
from .models import Student
from datetime import datetime


class StudentSerializer(serializers.ModelSerializer):

    _class = serializers.SerializerMethodField(read_only=True)
    age = serializers.SerializerMethodField(read_only=True)
    department = serializers.StringRelatedField()

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'middle_name', 'sex',
                  'department', '_class', 'admission_year', 'age', 'image']

    def get_age(self, student: Student):
        return datetime.now().year - student.birth_date.year

    def get__class(self, student: Student):
        return f'{student._class} {student.class_arm}'


class AddStudentSerializer(serializers.ModelSerializer):
    _class_id = serializers.IntegerField()
    class_arm_id = serializers.IntegerField()
    department_id = serializers.IntegerField()

    class Meta:
        model = Student
        fields = ['birth_date', 'sex', '_class_id', 'class_arm_id',
                  'department_id', 'admission_year', 'image']
