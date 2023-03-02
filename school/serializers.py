from rest_framework import serializers
from .models import AttendanceMark, Score, Student, Teacher
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
        return f'{teacher.managed_class} {teacher.managed_class_arm}'


class AddTeacherSerializer(serializers.ModelSerializer):
    subject_id = serializers.IntegerField()
    managed_class_id = serializers.IntegerField(required=False)
    managed_class_arm_id = serializers.IntegerField(required=False)

    def validate(self, attrs):
        class_id = attrs['managed_class_id']
        class_arm_id = attrs['managed_class_arm_id']
        if Teacher.objects.filter(managed_class_id=class_id, managed_class_arm_id=class_arm_id).exists():
            raise serializers.ValidationError(
                {'error': 'Different teacher already assigned to the specified class.'})
        return attrs

    class Meta:
        model = Teacher
        fields = ['id', 'birth_date', 'sex',
                  'managed_class_id', 'managed_class_arm_id', 'subject_id', 'image']


class ScoreSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()
    teacher = serializers.StringRelatedField()
    type = serializers.StringRelatedField()
    session = serializers.StringRelatedField()
    term = serializers.StringRelatedField()

    class Meta:
        model = Score
        fields = ['id', 'value', 'teacher', 'student', 'type', 'session', 'term',
                  ]


class AddScoreSerializer(serializers.ModelSerializer):
    student_id = serializers.IntegerField()
    type_id = serializers.IntegerField()
    session_id = serializers.IntegerField()
    term_id = serializers.IntegerField()

    def validate(self, attrs):
        fields = {
            'type': attrs['type_id'],
            'student': attrs['student_id'],
            'teacher': attrs['teacher_id'],
            'term': attrs['term_id'],
            'session': attrs['session_id']}
        MIN_SCORE = 30
        if fields['type'] == 1 and attrs['value'] > MIN_SCORE:
            raise serializers.ValidationError(
                {'error': f'CA score cannot be greater than {MIN_SCORE}'})

        if Score.objects.filter(**fields).exists():
            test_types = {
                1: 'CA', 2: 'EXAM'
            }
            raise serializers.ValidationError(
                {'error': f'Student already has {test_types[fields["type"]]} Score for this subject in this term.'})

        return super().validate(attrs)

    def create(self, validated_data):
        teacher_id = self.context['teacher_id']
        instance = Score.objects.create(
            **validated_data, teacher_id=teacher_id)
        return self.instance

    class Meta:
        model = Score
        fields = ['value', 'student_id', 'type_id', 'session_id', 'term_id']


class AttendanceMarkSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()
    student_id = serializers.IntegerField()

    def create(self, validated_data):
        teacher_id = Teacher.objects.only(
            'id').get(user_id=self.context['user_id'])
        print(teacher_id)
        return AttendanceMark.objects.create(**validated_data, class_teacher=teacher_id)

    class Meta:
        model = AttendanceMark
        fields = ['id', 'present', 'student', 'student_id',
                  'date_marked', 'week', 'day']
