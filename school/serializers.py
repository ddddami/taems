from rest_framework import serializers
from .models import Student, Teacher
from datetime import datetime


def age(student):
    return datetime.now().year - student.birth_date.year


class StudentSerializer(serializers.ModelSerializer):

    _class = serializers.SerializerMethodField(read_only=True)
    age = serializers.SerializerMethodField(read_only=True)
    department = serializers.StringRelatedField()
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'middle_name', 'user_id', 'sex',
                  'department', '_class', 'admission_year', 'age', 'image']

    def get_age(self, student: Student):
        age(student)

    def get__class(self, student: Student):
        return f'{student._class} {student.class_arm}'


class AddStudentSerializer(serializers.ModelSerializer):
    class_id = serializers.IntegerField(source='_class_id')
    class_arm_id = serializers.IntegerField()
    department_id = serializers.IntegerField()

    class Meta:
        model = Student
        fields = ['birth_date', 'sex', 'class_id', 'class_arm_id',
                  'department_id', 'admission_year', 'image']


class TeacherSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    age = serializers.SerializerMethodField()
    managed_class = serializers.SerializerMethodField()
    taught_subject = serializers.StringRelatedField(source='subject')

    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name',
                  'middle_name', 'user_id', 'sex', 'birth_date', 'age', 'managed_class', 'taught_subject', 'image']

    def get_age(self, student: Student):
        age(student)

    def get_managed_class(self, teacher: Teacher):
        return f'{teacher._class} {teacher.class_arm}'


class AddTeacherSerializer(serializers.ModelSerializer):
    subject_id = serializers.IntegerField()
    managed_class_id = serializers.IntegerField(
        source='_class_id', required=False)
    managed_class_arm_id = serializers.IntegerField(
        source='class_arm_id', required=False)

    def validate(self, attrs):
        class_id = attrs['_class_id']
        class_arm_id = attrs['class_arm_id']
        if Teacher.objects.filter(_class_id=class_id, class_arm_id=class_arm_id).exists():
            raise serializers.ValidationError(
                {'error': 'Different teacher already assigned to the specified class.'})
        return attrs

    class Meta:
        model = Teacher
        fields = ['id', 'birth_date', 'sex',
                  'managed_class_id', 'managed_class_arm_id', 'subject_id', 'image']
