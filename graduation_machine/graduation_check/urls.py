from django.urls import path
from .views import GraduationRequirementsViewSet
from .views import LectureGroupViewSet

urlpatterns = [
    path('graduation_conditions', GraduationRequirementsViewSet.as_view({'get': 'list'})),
    path('common_lecture_groups', LectureGroupViewSet.as_view({'get': 'list'})),
]