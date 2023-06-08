from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from school.models import Student, Teacher, School
from location.models import Address
from .serializers import AddressSerializer, CreateAddressSerializer

# Create your views here.


class AddressAPIView(APIView):
    def post(self, request):
        serializer = CreateAddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, **kwargs):
        obj_type = self.kwargs['obj_type']
        content_types = {
            'student': Student,
            'teacher': Teacher,
            'school': School
        }
        content_type = content_types[obj_type]
        if not obj_type in content_types.keys():
            return Response('Invalid object type.', status=status.HTTP_400_BAD_REQUEST)
        obj_id = request.user.student.id
        queryset = Address.objects.get_address_for(
            content_type, obj_id).first()
        print(queryset)
        serializer = AddressSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
