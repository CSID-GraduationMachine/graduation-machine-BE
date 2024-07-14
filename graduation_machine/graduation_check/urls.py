from django.urls import path
from .views import GraduationRequirementsViewSet

urlpatterns = [
    path('graduation_conditions', GraduationRequirementsViewSet.as_view({'get': 'list'})),
]
