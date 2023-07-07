from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('students', views.StudentViewSet, basename='student')
router.register('teachers', views.TeacherViewSet, basename='teacher')
router.register('scores', views.ScoreViewSet, basename='score')
router.register('attendance-marks',
                views.AttendanceMarkViewSet, basename='attendance')
router.register('subjects', views.SubjectViewSet, basename='subject')

urlpatterns = router.urls
