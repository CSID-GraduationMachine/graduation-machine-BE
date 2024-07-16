from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import  GraduationRequirementsViewSet, GraduationRequirementsDetailViewSet, LectureLectureGroupViewSet, PrerequestViewSet, LectureGroupViewSet, CommonLectureGroupViewSet, CommonLectureGroupLectureViewSet

router = SimpleRouter()

urlpatterns = [
    # 졸업 요건
    path('graduation-requirements', GraduationRequirementsViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('graduation-requirements/<int:requirements_pk>', GraduationRequirementsViewSet.as_view({'delete': 'destroy', 'patch': 'update'})),

    # 졸업 요건 상세
    path('graduation-requirements/<int:requirements_pk>/graduation-requirements-details', GraduationRequirementsDetailViewSet.as_view({'get':'list', 'post': 'create'})),
    path('graduation-requirements/<int:requirements_pk>/graduation-requirements-details/<int:requirements_details_pk>', GraduationRequirementsDetailViewSet.as_view({'delete': 'destroy', 'patch': 'update'})),

    # 선택한 졸업 요건 상세에 포함된 강의 그룹
    path('graduation-requirements/<int:requirements_pk>/graduation-requirements-details/<int:requirements_details_pk>/lecture-groups', LectureGroupViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('graduation-requirements/<int:requirements_pk>/graduation-requirements-details/<int:requirements_details_pk>/lecture-groups/<int:lecture_groups_pk>', LectureGroupViewSet.as_view({'delete': 'destroy', 'patch': 'update'})),

    # 선이수
    path('graduation-requirements/<int:requirements_pk>/graduation-requirements-details/<int:requirements_details_pk>/lecture-groups/<int:lecture_groups_pk>/prerequests', PrerequestViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('graduation-requirements/<int:requirements_pk>/graduation-requirements-details/<int:requirements_details_pk>/lecture-groups/<int:lecture_groups_pk>/prerequests/<int:prerequests_pk>', PrerequestViewSet.as_view({'delete': 'destroy'})),

    # 선택한 강의 그룹의 강의
    path('graduation-requirements/<int:requirements_pk>/graduation-requirements-details/<int:requirements_details_pk>/lecture-groups/<int:lecture_groups_pk>/lectures', LectureLectureGroupViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('graduation-requirements/<int:requirements_pk>/graduation-requirements-details/<int:requirements_details_pk>/lecture-groups/<int:lecture_groups_pk>/lectures/<int:lecture_lecturegroups_pk>', LectureLectureGroupViewSet.as_view({'delete': 'destroy'})),

    # 공통 강의 그룹
    path('common-lecture-groups', CommonLectureGroupViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('common-lecture-groups/<int:common_lecture_groups_pk>', CommonLectureGroupViewSet.as_view({'delete': 'destroy', 'patch': 'update'})),

    # 공통 강의 그룹에 포함된 강의
    path('common-lecture-groups/<int:common_lecture_groups_pk>/lectures', CommonLectureGroupLectureViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('common-lecture-groups/<int:common_lecture_groups_pk>/lectures/<int:lectures_pk>', CommonLectureGroupLectureViewSet.as_view({'delete': 'destroy'})),
]