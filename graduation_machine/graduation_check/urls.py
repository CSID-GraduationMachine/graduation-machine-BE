from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import  GraduationRequirementsViewSet, GraduationRequirementsDetailViewSet, LectureLectureGroupViewSet, PrerequestViewSet, LectureGroupViewSet, CommonLectureGroupViewSet, CommonLectureGroupLectureViewSet, GraduationCheckAPIView

router = SimpleRouter()

urlpatterns = [
    # 졸업 요건
    path('graduation-requirements', GraduationRequirementsViewSet.as_view({'get': 'list', 'post': 'create'}), name='졸업 요건'),
    path('graduation-requirements/<int:requirements_pk>', GraduationRequirementsViewSet.as_view({'delete': 'destroy', 'patch': 'update'}),name='졸업 요건'),

    # 졸업 요건 상세
    path('graduation-requirements/<int:requirements_pk>/details', GraduationRequirementsDetailViewSet.as_view({'get':'list', 'post': 'create'}), name='졸업 요건 상세'),
    path('graduation-requirements/<int:requirements_pk>/details/<int:requirements_details_pk>', GraduationRequirementsDetailViewSet.as_view({'delete': 'destroy', 'patch': 'update'}),name='졸업 요건 상세'),

    # 선택한 졸업 요건 상세에 포함된 강의 그룹
    path('details/<int:requirements_details_pk>/lecture-groups', LectureGroupViewSet.as_view({'get': 'list', 'post': 'create'}), name='강의 그룹'),
    path('details/<int:requirements_details_pk>/lecture-groups/<int:groups_pk>', LectureGroupViewSet.as_view({'delete': 'destroy', 'patch': 'update'}), name='강의 그룹'),

    # 선이수
    path('lecture-groups/<int:groups_pk>/prerequests', PrerequestViewSet.as_view({'get': 'list', 'post': 'create'}), name='선이수'),
    path('lecture-groups/<int:groups_pk>/prerequests/<int:prerequests_pk>', PrerequestViewSet.as_view({'delete': 'destroy'}),name='선이수'),

    # 선택한 강의 그룹의 강의
    path('lecture-groups/<int:groups_pk>/lectures', LectureLectureGroupViewSet.as_view({'get': 'list', 'post': 'create'}), name='강의 그룹에 포함된 강의'),
    path('lecture-groups/<int:groups_pk>/lectures/<int:lectures_pk>', LectureLectureGroupViewSet.as_view({'delete': 'destroy'}), name='강의 그룹에 포함된 강의'),

    # 공통 강의 그룹
    path('common-lecture-groups', CommonLectureGroupViewSet.as_view({'get': 'list', 'post': 'create'}),name='공통 강의 그룹'),
    path('common-lecture-groups/<int:groups_pk>', CommonLectureGroupViewSet.as_view({'delete': 'destroy', 'patch': 'update'}),name='공통 강의 그룹'),

    # 공통 강의 그룹에 포함된 강의
    path('common-lecture-groups/<int:groups_pk>/lectures', CommonLectureGroupLectureViewSet.as_view({'get': 'list', 'post': 'create'}),name='공통 강의 그룹에 포함된 강의'),
    path('common-lecture-groups/<int:groups_pk>/lectures/<int:lectures_pk>', CommonLectureGroupLectureViewSet.as_view({'delete': 'destroy'}),name='공통 강의 그룹에 포함된 강의'),

    # 졸업 요건 검사
    path('graduation-check', GraduationCheckAPIView.as_view(), name='졸업 요건 검사'),
]