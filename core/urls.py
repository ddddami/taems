from django.urls import path
from . import views
urlpatterns = [
    path('addresses/<obj_type>/', views.AddressAPIView.as_view())
]
