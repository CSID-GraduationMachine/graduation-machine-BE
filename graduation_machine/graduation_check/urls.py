from django.urls import path
from .views import GraduationRequirementsViewSet
from .views import LectureGroupViewSet
from .views import LectureViewSet

urlpatterns = [
    path('graduation_conditions', GraduationRequirementsViewSet.as_view({'get': 'list'})),
    path('common_lecture_groups', LectureGroupViewSet.as_view({'get': 'list'})),
    path('common_lecture_descriptions', LectureViewSet.as_view({'get': 'list'})),
]