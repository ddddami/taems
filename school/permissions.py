from rest_framework import permissions
from school.models import Teacher


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class FullDjangoModelPermission(permissions.DjangoModelPermissions):
    def __init__(self) -> None:
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']


class IsSchoolMember(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        school_id = Teacher.objects.get(user_id=request.user.id).school.id
        if school_id == obj.school_id:
            return True
        return False


class IsOfStudentSchool(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        school_id = Teacher.objects.get(user_id=request.user.id).school.id
        if school_id == obj.student.school_id:
            return True
        return False
