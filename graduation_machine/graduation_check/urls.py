from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import  GraduationRequirementsViewSet, GraduationRequirementsDetailViewSet, LectureLectureGroupViewSet, PrerequestViewSet, LectureGroupViewSet, CommonLectureGroupViewSet, CommonLectureGroupLectureViewSet
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="graduation_machine API",
        default_version='프로젝트 버전(예: 1.0.0)',
        description="graduation_machine API 문서",
        terms_of_service="https://www.google.com/policies/terms/",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = SimpleRouter()

urlpatterns = [
    # 졸업 요건
    path('graduation-requirements', GraduationRequirementsViewSet.as_view({'get': 'list', 'post': 'create'}), name='graduation-requirements'),
    path('graduation-requirements/<int:requirements_pk>', GraduationRequirementsViewSet.as_view({'delete': 'destroy', 'patch': 'update'}),name='graduation-requirements'),

    # 졸업 요건 상세
    path('graduation-requirements/<int:requirements_pk>/graduation-requirements-details', GraduationRequirementsDetailViewSet.as_view({'get':'list', 'post': 'create'}), name='graduation-requirements-details'),
    path('graduation-requirements/<int:requirements_pk>/graduation-requirements-details/<int:requirements_details_pk>', GraduationRequirementsDetailViewSet.as_view({'delete': 'destroy', 'patch': 'update'}),name='graduation-requirements-details'),

    # 선택한 졸업 요건 상세에 포함된 강의 그룹
    path('graduation-requirements/<int:requirements_pk>/graduation-requirements-details/<int:requirements_details_pk>/lecture-groups', LectureGroupViewSet.as_view({'get': 'list', 'post': 'create'}), name='lecture-groups'),
    path('graduation-requirements/<int:requirements_pk>/graduation-requirements-details/<int:requirements_details_pk>/lecture-groups/<int:lecture_groups_pk>', LectureGroupViewSet.as_view({'delete': 'destroy', 'patch': 'update'}), name='lecture-groups'),

    # 선이수
    path('graduation-requirements/<int:requirements_pk>/graduation-requirements-details/<int:requirements_details_pk>/lecture-groups/<int:lecture_groups_pk>/prerequests', PrerequestViewSet.as_view({'get': 'list', 'post': 'create'}), name='prerequests'),
    path('graduation-requirements/<int:requirements_pk>/graduation-requirements-details/<int:requirements_details_pk>/lecture-groups/<int:lecture_groups_pk>/prerequests/<int:prerequests_pk>', PrerequestViewSet.as_view({'delete': 'destroy'}),name='prerequests'),

    # 선택한 강의 그룹의 강의
    path('graduation-requirements/<int:requirements_pk>/graduation-requirements-details/<int:requirements_details_pk>/lecture-groups/<int:lecture_groups_pk>/lectures', LectureLectureGroupViewSet.as_view({'get': 'list', 'post': 'create'}), name='lectures-in-lecturegroup'),
    path('graduation-requirements/<int:requirements_pk>/graduation-requirements-details/<int:requirements_details_pk>/lecture-groups/<int:lecture_groups_pk>/lectures/<int:lecture_lecturegroups_pk>', LectureLectureGroupViewSet.as_view({'delete': 'destroy'}), name='lectures-in-lecturegroup'),

    # 공통 강의 그룹
    path('common-lecture-groups', CommonLectureGroupViewSet.as_view({'get': 'list', 'post': 'create'}),name='common-lecture-groups'),
    path('common-lecture-groups/<int:common_lecture_groups_pk>', CommonLectureGroupViewSet.as_view({'delete': 'destroy', 'patch': 'update'}),name='common-lecture-groups'),

    # 공통 강의 그룹에 포함된 강의
    path('common-lecture-groups/<int:common_lecture_groups_pk>/lectures', CommonLectureGroupLectureViewSet.as_view({'get': 'list', 'post': 'create'}),name='lecture-in-common-lecture-group'),
    path('common-lecture-groups/<int:common_lecture_groups_pk>/lectures/<int:lectures_pk>', CommonLectureGroupLectureViewSet.as_view({'delete': 'destroy'}),name='lecture-in-common-lecture-group'),
]