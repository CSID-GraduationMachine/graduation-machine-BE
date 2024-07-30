from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import ConditionViewSet, LectureConditionViewSet, LectureIdentificationLectureGroupViewSet, PrerequestViewSet, LectureGroupViewSet, CommonLectureGroupViewSet, CommonLectureGroupLectureIdentificationViewSet, GraduationCheckAPIView
from .views import LectureIdentificationAPIView
from .views import LectureGroupForAddPrerequestAPIView
router = SimpleRouter()

urlpatterns = [
    # 졸업 요건
    path('conditions', ConditionViewSet.as_view({'get': 'list', 'post': 'create'}), name='졸업 요건'),
    path('conditions/<int:conditions_pk>', ConditionViewSet.as_view({'delete': 'destroy', 'patch': 'update'}),name='졸업 요건'),

    # 졸업 요건 상세
    path('conditions/<int:conditions_pk>/lecture-conditions', LectureConditionViewSet.as_view({'get':'list', 'post': 'create'}), name='졸업 요건 상세'),
    path('conditions/<int:conditions_pk>/lecture-conditions/<int:lecture_conditions_pk>', LectureConditionViewSet.as_view({'delete': 'destroy', 'patch': 'update'}),name='졸업 요건 상세'),

    # 선택한 졸업 요건 상세에 포함된 강의 그룹
    path('lecture-conditions/<int:lecture_conditions_pk>/lecture-groups', LectureGroupViewSet.as_view({'get': 'list', 'post': 'create'}), name='강의 그룹'),
    path('lecture-conditions/<int:lecture_conditions_pk>/lecture-groups/<int:groups_pk>', LectureGroupViewSet.as_view({'delete': 'destroy', 'patch': 'update'}), name='강의 그룹'),
    # 선이수 추가를 위한 강의그룹 조회 (자기자신 제외, 이미 추가된 강의그룹 제외)
    path('lecture-conditions/<int:lecture_conditions_pk>/lecture-groups-for-prerequest/<int:groups_pk>', LectureGroupForAddPrerequestAPIView.as_view(), name='선이수 추가를 위한 강의그룹 조회'),

    # 선이수
    path('lecture-groups/<int:groups_pk>/prerequests', PrerequestViewSet.as_view({'get': 'list', 'post': 'create'}), name='선이수'),
    path('lecture-groups/<int:groups_pk>/prerequests/<int:prerequests_pk>', PrerequestViewSet.as_view({'delete': 'destroy'}),name='선이수'),

    # 선택한 강의 그룹의 강의
    path('lecture-groups/<int:groups_pk>/lectures', LectureIdentificationLectureGroupViewSet.as_view({'get': 'list', 'post': 'create'}), name='강의 그룹에 포함된 강의'),
    path('lecture-groups/<int:groups_pk>/lectures/<int:lectures_pk>', LectureIdentificationLectureGroupViewSet.as_view({'delete': 'destroy'}), name='강의 그룹에 포함된 강의'),

    # 공통 강의 그룹
    path('common-lecture-groups', CommonLectureGroupViewSet.as_view({'get': 'list', 'post': 'create'}),name='공통 강의 그룹'),
    path('common-lecture-groups/<int:groups_pk>', CommonLectureGroupViewSet.as_view({'delete': 'destroy', 'patch': 'update'}),name='공통 강의 그룹'),

    # 공통 강의 그룹에 포함된 강의
    path('common-lecture-groups/<int:groups_pk>/lectures', CommonLectureGroupLectureIdentificationViewSet.as_view({'get': 'list', 'post': 'create'}),name='공통 강의 그룹에 포함된 강의'),
    path('common-lecture-groups/<int:groups_pk>/lectures/<int:lectures_pk>', CommonLectureGroupLectureIdentificationViewSet.as_view({'delete': 'destroy'}),name='공통 강의 그룹에 포함된 강의'),

    # 졸업 요건 검사
    path('graduation-check', GraduationCheckAPIView.as_view(), name='졸업 요건 검사'),

    # LectureIdentification 조회
    path('lecture-identifications', LectureIdentificationAPIView.as_view(), name='강의 조회'),
]