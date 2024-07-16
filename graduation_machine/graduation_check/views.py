from rest_framework import viewsets, mixins, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from .serializers import (
    GraduationRequirementsDetailSerializer,
    LectureGroupSerializer,
    LectureSerializer,
    LectureLectureGroupSerializer,
    PrerequestSerializer,
    CommonLectureGroupSerializer,
    GraduationRequirementsSerializer,
    CommonLectureGroupLectureSerializer
)
from .models import GraduationRequirementsDetail
from .services.common_lecture_group_lecture_service import CommonLectureGroupLectureService
from .services.graduation_requirements_service import GraduationRequirementService
from .services.graduation_requirements_detail_service import GraduationRequirementDetailService
from .services.lecture_lecture_group_service import LectureLectureGroupService
from .services.lecture_group_service import LectureGroupService
from .services.lecture_service import LectureService
from .services.prerequest_service import PrerequestService
from .services.common_lecture_group_service import CommonLectureGroupService
from .services.graduation_check_service import GraduationCheckService

class GraduationRequirementsViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin
):
    serializer_class = GraduationRequirementsSerializer

    def list(self, request, *args, **kwargs):
        """
        졸업 요건 조회
        """
        requirements = GraduationRequirementService.get_graduation_requirements()
        return Response({"success": True, "data": GraduationRequirementsSerializer(requirements, many=True).data, "error": None})

    def create(self, request, *args, **kwargs):
        """
        졸업 요건 생성
        """
        year = request.data.get('year')
        tech = request.data.get('tech')
        total_minimum_credit = request.data.get('total_minimum_credit')
        GraduationRequirementService.create_graduation_requirements(year, tech, total_minimum_credit)
        return Response({"success": True, "data": None, "error": None})

    def destroy(self, request, *args, **kwargs):
        """
        졸업 요건 삭제
        """
        requirement_id = kwargs.get('requirements_pk')
        GraduationRequirementService.delete_graduation_requirements(requirement_id)
        return Response({"success": True, "data": None, "error": None})

    def update(self, request, *args, **kwargs):
        """
        졸업 요건 수정
        """
        requirement_id = kwargs.get('requirements_pk')
        year = request.data.get('year')
        tech = request.data.get('tech')
        total_minimum_credit = request.data.get('total_minimum_credit')
        GraduationRequirementService.update_graduation_requirements(requirement_id, year, tech, total_minimum_credit)
        return Response({"success": True, "data": None, "error": None})

class GraduationRequirementsDetailViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin
    ):

    serializer_class = GraduationRequirementsDetailSerializer

    def list(self, request, *args, **kwargs):
        """
        졸업 요건 상세 조회
        """
        requirements_id = kwargs.get('requirements_pk')
        details = GraduationRequirementDetailService.get_graduation_requirements_details(requirements_id)
        total_minimum_credit = GraduationRequirementService.get_total_minimum_credit(requirements_id)
        
        serialized_data = GraduationRequirementsDetailSerializer(details, many=True).data
        
        response_data = {
            "success": True,
            "data": {
                "total_minimum_credit": total_minimum_credit,
                "requirements": serialized_data
            },
            "error": None
        }

        return Response(response_data)
        
    def create(self, request, *args, **kwargs):
        """
        졸업 요건 상세 생성
        """
        requirement_id = kwargs.get('requirements_pk')
        requirement_name = request.data.get('requirements_name')
        minimum_credit = request.data.get('minimum_credit')
        GraduationRequirementDetailService.create_graduation_conditions(requirement_id, requirement_name, minimum_credit)
        return Response({"success": True, "data": None, "error": None})
        
    def update(self, request, *args, **kwargs):
        """
        졸업 요건 상세 수정
        """
        requirement_detail_id = kwargs.get('requirements_details_pk')
        requirements_name = request.data.get('requirements_name')
        minimum_credit = request.data.get('minimum_credit')
        GraduationRequirementDetailService.update_graduation_conditions(requirement_detail_id, requirements_name, minimum_credit)
        return Response({"success": True, "data": None, "error": None})
    
    def destroy(self, request, *args, **kwargs):
        """
        졸업 요건 상세 삭제
        """
        requirement_detail_id = kwargs.get('requirements_details_pk')
        GraduationRequirementDetailService.delete_graduation_conditions(requirement_detail_id)
        return Response({"success": True, "data": None, "error": None})


class LectureGroupViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin
    ):
    serializer_class = LectureGroupSerializer

    def list(self, request, *args, **kwargs):
        """
        선택한 졸업 요건 상세에 포함된 강의 그룹 조회
        """
        requirements_detail_id = kwargs.get('requirements_details_pk')
        lecture_groups = LectureGroupService.get_lecture_groups(requirements_detail_id)
        return Response({"success": True, "data": LectureGroupSerializer(lecture_groups, many=True).data, "error": None})
    def create(self, request, *args, **kwargs):
        """
        선택한 졸업 요건 상세에 포함된 강의 그룹 생성
        """
        requirements_detail_id = kwargs.get('requirements_details_pk')
        lecture_group_name = request.data.get('lecture_group_name')
        is_essential = request.data.get('is_essential')
        LectureGroupService.create_lecture_group(requirements_detail_id, lecture_group_name, is_essential)
        return Response({"success": True, "data": None, "error": None})
    def update(self, request, *args, **kwargs):
        """
        선택한 졸업 요건 상세에 포함된 강의 그룹 수정
        """
        lecture_group_id = kwargs.get('lecture_groups_pk')
        lecture_group_name = request.data.get('lecture_group_name')
        LectureGroupService.update_lecture_group(lecture_group_id, lecture_group_name)
        return Response({"success": True, "data": None, "error": None})
    def destroy(self, request, *args, **kwargs):
        """
        선택한 졸업 요건 상세에 포함된 강의 그룹 삭제
        """
        lecture_group_id = kwargs.get('lecture_groups_pk')
        LectureGroupService.delete_lecture_group(lecture_group_id)
        return Response({"success": True, "data": None, "error": None})


class LectureLectureGroupViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin
    ):
    serializer_class = LectureLectureGroupSerializer

    def list(self, request, *args, **kwargs):
        """
        선택한 강의 그룹의 강의 조회
        """
        lecture_group_id = kwargs.get('lecture_groups_pk')
        lecture_lecturegroups = LectureLectureGroupService.get_lecture_lecturegroups(lecture_group_id)
        return Response({"success": True, "data": LectureLectureGroupSerializer(lecture_lecturegroups, many=True).data, "error": None})
    def create(self, request, *args, **kwargs):
        """
        선택한 강의 그룹의 강의 생성
        """
        lecture_group_id = kwargs.get('lecture_groups_pk')
        lecture_id = request.data.get('lecture_id')
        LectureLectureGroupService.create_lecture_lecturegroup(lecture_group_id, lecture_id)
        return Response({"success": True, "data": None, "error": None})
    def destroy(self, request, *args, **kwargs):
        """
        선택한 강의 그룹의 강의 삭제
        """
        lecture_lecturegroups_id = kwargs.get('lecture_lecturegroups_pk')
        LectureLectureGroupService.delete_lecture_lecturegroup(lecture_lecturegroups_id)
        return Response({"success": True, "data": None, "error": None})
    


class PrerequestViewSet(viewsets.GenericViewSet, 
                        mixins.ListModelMixin, 
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin):
    def list(self, request, *args, **kwargs):
        """
        선이수 조회
        """
        lecture_group_id = kwargs.get('lecture_groups_pk')
        prerequests = PrerequestService.get_prerequests(lecture_group_id)

        response_data = {
            "success": True,
            "data": PrerequestSerializer(prerequests, many=True).data,
            "error": None
        }
        return Response(response_data)
    
    def create(self, request, *args, **kwargs):
        """
        선이수 생성
        """
        lecture_group_id = kwargs.get('lecture_groups_pk')
        prerequst_lecture_group_id = request.data.get('prerequest_lecture_group_id')
        PrerequestService.create_prerequest(lecture_group_id, prerequst_lecture_group_id)
        return Response({"success": True, "data": None, "error": None})
    
    def destroy(self, request, *args, **kwargs):
        """
        선이수 삭제
        """
        id = kwargs.get('prerequests_pk')
        PrerequestService.delete_prerequest(id)
        return Response({"success": True, "data": None, "error": None})
    


class CommonLectureGroupViewSet(viewsets.GenericViewSet, 
                                mixins.ListModelMixin, 
                                mixins.CreateModelMixin, 
                                mixins.DestroyModelMixin,
                                mixins.UpdateModelMixin):
    
    serializer_class = CommonLectureGroupSerializer

    def list(self, request, *args, **kwargs):
        """
        공통 강의 그룹 조회
        """
        common_lectures = CommonLectureGroupService.get_all_common_lectures()
        return Response({"success": True, "data": CommonLectureGroupSerializer(common_lectures, many=True).data, "error": None})

    def create(self, request, *args, **kwargs):
        """
        공통 강의 그룹 생성
        """
        common_group_name = request.data.get('common_group_name')
        CommonLectureGroupService.create_common_lecture_group(common_group_name)
        return Response({"success": True, "data": None, "error": None})
    
    def update(self, request, *args, **kwargs):
        """
        공통 강의 그룹 수정
        """
        common_lecture_group_id = kwargs.get('common_lecture_groups_pk')
        common_group_name = request.data.get('common_group_name')
        CommonLectureGroupService.update_common_lecture_group(common_lecture_group_id, common_group_name)
        return Response({"success": True, "data": None, "error": None})

    def destroy(self, request, *args, **kwargs):
        """
        공통 강의 그룹 삭제
        """
        common_lecture_group_id = kwargs.get('common_lecture_groups_pk')
        CommonLectureGroupService.delete_common_lecture_group(common_lecture_group_id)
        return Response({"success": True, "data": None, "error": None})
    
class CommonLectureGroupLectureViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin
    ):
    serializer_class = CommonLectureGroupLectureSerializer

    def list(self, request, *args, **kwargs):
        """
        공통 강의 그룹에 포함된 강의 조회
        """
        common_lecture_group_id = kwargs.get('common_lecture_groups_pk')
        common_lecture_group_lecture = CommonLectureGroupLectureService.get_lectures(common_lecture_group_id)
        return Response({"success": True, "data": CommonLectureGroupLectureSerializer(common_lecture_group_lecture, many=True).data, "error": None})
    def create(self, request, *args, **kwargs):
        """
        공통 강의 그룹에 포함된 강의 생성
        """
        common_lecture_group_id = kwargs.get('common_lecture_groups_pk')
        lecture_id = request.data.get('lecture_id')
        CommonLectureGroupLectureService.create_common_lecture_group_lecture(common_lecture_group_id, lecture_id)
        return Response({"success": True, "data": None, "error": None})
    def destroy(self, request, *args, **kwargs):
        """
        공통 강의 그룹에 포함된 강의 삭제
        """

        lecture_id = kwargs.get('lectures_pk')
        CommonLectureGroupLectureService.delete_common_lecture_group_lecture(lecture_id)
        return Response({"success": True, "data": None, "error": None})

class GraduationCheckAPIView(views.APIView):

    def post(self, request, *args, **kwargs):
        year = self.request.query_params.get('year')
        tech = self.request.query_params.get('tech')
        excel_file = request.FILES.get('file')

        if not excel_file.name.endswith('.xlsx'):
            return JsonResponse({'error': 'File is not xlsx format'}, status=400)
        
        return Response({"success": True, "data": GraduationCheckService().check_graduation(year, tech, excel_file), "error": None})
