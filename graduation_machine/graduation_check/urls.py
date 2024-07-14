from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import GraduationRequirementsViewSet, LectureGroupViewSet, LectureViewSet, PrerequestViewSet, CommonLectureGroupViewSet, GraduationCheckAPIView, LecturesInCommonGroupAPIView

router = SimpleRouter()

urlpatterns = [
    # 학과 년도별 졸업이수 조건 조회
    path('graduation-conditions', GraduationRequirementsViewSet.as_view({'get': 'list'})),
    # 해당 조건 공통강의 그룹 조회
    path('common-lecture-groups', LectureGroupViewSet.as_view({'get': 'list'})),
    # 공통강의 개설 강의 내역 조회
    path('common-lecture-descriptions', LectureViewSet.as_view({'get': 'list'})),
    # 선이수 목록 조회, 추가
    path('prerequests', PrerequestViewSet.as_view({'get': 'list', 'post': 'create'})),
    # 공통 강의 그룹 조회, 추가, 삭제
    path('common-lecture-group', CommonLectureGroupViewSet.as_view({'get': 'list', 'post': 'create', 'delete': 'destroy'})),
    # 특정 공통 강의 그룹에 속한 강의들 조회
    path('common-lecture-group/lectures', LecturesInCommonGroupAPIView.as_view(), name='common-lecture-group-lectures'),
    # 졸업 요건 만족 검사
    path('check', GraduationCheckAPIView.as_view(), name='graduation-check'),
]