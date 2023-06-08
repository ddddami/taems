from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from school.models import Student, Teacher, School
from location.models import Address


class AddressSerializer(serializers.ModelSerializer):
    city = serializers.CharField()
    street = serializers.CharField()
    lga = serializers.StringRelatedField()
    state = serializers.SerializerMethodField()

    def get_state(self, address):
        return str(address.lga.state)

    class Meta:
        model = Address
        fields = ['city', 'street', 'lga', 'state']


class CreateAddressSerializer(serializers.ModelSerializer):
    street = serializers.CharField()
    city = serializers.CharField()
    object_type = serializers.CharField(source='content_type')
    object_id = serializers.IntegerField()
    lga_id = serializers.IntegerField()

    class Meta:
        model = Address
        fields = ['id', 'street', 'city', 'lga_id', 'object_type',
                  'object_id']

    def validate_object_type(self, object_type):
        if object_type not in ['student', 'teacher', 'school']:
            raise serializers.ValidationError('Invalid object type')
        return object_type

    def create(self, validated_data):
        object_type = self.validated_data['content_type']
        if object_type == 'student':
            model = Student
        elif object_type == 'teacher':
            model = Teacher
        else:
            model = School
        content_type = ContentType.objects.get_for_model(model)
        validated_data["content_type"] = content_type

        return super().create(validated_data)
