from django.urls import path
from .views import GraduationCheckAPIView
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

urlpatterns = [
    path('check', GraduationCheckAPIView.as_view(), name='graduation-check'),
]