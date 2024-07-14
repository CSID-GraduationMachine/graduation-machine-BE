from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import GraduationRequirementsDetailViewSet, LectureViewSet, PrerequestViewSet, CommonLectureGroupViewSet, GraduationCheckAPIView, LecturesInCommonGroupAPIView

router = SimpleRouter()

urlpatterns = [
    # 학과 년도별 졸업이수 요건 조회
    path('graduation-requirements-detail', GraduationRequirementsDetailViewSet.as_view({'get': 'list', 'post': 'create', 'delete': 'destroy', 'patch': 'update'})),

    # 특정 졸업 요건의 강의 그룹 조회
    path('graduation-requirements-detail/<int:pk>/lecture-groups', GraduationRequirementsDetailViewSet.as_view({'get': 'list'})),

    # 강의추가


    # 강의 그룹내 강의 조회, 강의 그룹내 강의 추가, 강의 그룹내 강의 삭제
    path('lecture-groups/lectures', LectureViewSet.as_view({'get': 'list', 'post': 'create', 'delete': 'destroy'})),


    # 선이수 목록 조회, 추가
    path('prerequests', PrerequestViewSet.as_view({'get': 'list', 'post': 'create'})),


    # 공통 강의 그룹 조회, 추가, 삭제
    path('common-lecture-groups', CommonLectureGroupViewSet.as_view({'get': 'list', 'post': 'create', 'delete': 'destroy'})),


    # 특정 공통 강의 그룹에 속한 강의들 조회
    path('common-lecture-groups/lectures', LecturesInCommonGroupAPIView.as_view(), name='common-lecture-group-lectures'),


    # 졸업 요건 만족 검사
    path('check', GraduationCheckAPIView.as_view(), name='graduation-check'),
]