from django.urls import path
from .views import GraduationRequirementsViewSet, LectureGroupViewSet, LectureViewSet, PrerequestViewSet, CommonLectureGroupViewSet

urlpatterns = [
    # 학과 년도별 졸업이수 조건 조회
    path('graduation_conditions', GraduationRequirementsViewSet.as_view({'get': 'list'})),
    # 해당 조건 공통강의 그룹 조회
    path('common_lecture_groups', LectureGroupViewSet.as_view({'get': 'list'})),
    # 공통강의 개설 강의 내역 조회
    path('common_lecture_descriptions', LectureViewSet.as_view({'get': 'list'})),
    # 선이수 목록 조회, 추가
    path('prerequests', PrerequestViewSet.as_view({'get': 'list', 'post': 'create'})),
    # 전체 공통 강의 조회
    path('all_common_lectures', CommonLectureGroupViewSet.as_view({'get': 'list'})),
    # 공통 강의 그룹 추가, 삭제
    path('common_lecture_group', CommonLectureGroupViewSet.as_view({'post': 'create', 'delete': 'destroy'})),
]
