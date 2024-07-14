from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    GraduationRequirementsDetailSerializer,
    LectureGroupSerializer,
    LectureSerializer,
    PrerequestSerializer,
    CommonLectureGroupSerializer,
)
from .services.graduation_requirements_service import GraduationRequirementService
from .services.lecture_group_service import LectureGroupService
from .services.lecture_service import LectureService
from .services.prerequest_service import PrerequestService
from .services.common_lecture_group_service import CommonLectureGroupService
from .models import GraduationRequirements


class GraduationRequirementsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = GraduationRequirementsDetailSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        year = request.query_params.get('year')
        tech = request.query_params.get('tech')
        requirements = GraduationRequirementService.get_graduation_conditions(year, tech)
        
        if requirements:
            details = GraduationRequirementService.get_graduation_requirements_details(requirements.id)
            response_data = {
                "entire_minimum_credit": requirements.total_minimum_credit,
                "details": GraduationRequirementsDetailSerializer(details, many=True).data
            }
            return Response({"success": True, "data": response_data, "error": None})
        else:
            return Response({"success": False, "error": "Graduation requirements not found"})

class LectureGroupViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = LectureGroupSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        requirement_id = request.query_params.get('id')
        groups = LectureGroupService.get_common_lecture_groups(requirement_id)
        return Response({"success": True, "data": LectureGroupSerializer(groups, many=True).data, "error": None})


class LectureViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = LectureSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        group_id = request.query_params.get('id')
        lectures = LectureService.get_common_lecture_descriptions(group_id)
        prelectures = PrerequestService.get_prerequests()
        prelecture_data = [
            {"pre_lecture_group_name": pre.prerequest_lecture_group.lecture_group_name,
             "pre_lecture_group_id": pre.prerequest_lecture_group.id}
            for pre in prelectures if pre.lecture_group.id == group_id
        ]
        lecture_data = LectureSerializer(lectures, many=True).data
        return Response({"success": True, "data": [prelecture_data, lecture_data], "error": None})


class PrerequestViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = PrerequestSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        prerequests = PrerequestService.get_prerequests()
        return Response({"success": True, "data": PrerequestSerializer(prerequests, many=True).data, "error": None})

    def create(self, request, *args, **kwargs):
        lecture_group_id = request.data.get('lecture_group_id')
        prerequest_lecture_group_id = request.data.get('prerequest_lecture_group_id')
        PrerequestService.add_prerequest(lecture_group_id, prerequest_lecture_group_id)
        return Response({"success": True, "data": None, "error": None})


class CommonLectureGroupViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    serializer_class = CommonLectureGroupSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        common_lectures = CommonLectureGroupService.get_all_common_lectures()
        return Response({"success": True, "data": CommonLectureGroupSerializer(common_lectures, many=True).data, "error": None})

    def create(self, request, *args, **kwargs):
        lecture_ids = request.data.get('lecture_id')
        common_group_name = request.data.get('lecture_group_name')
        CommonLectureGroupService.create_common_lecture_group(lecture_ids, common_group_name)
        return Response({"success": True, "data": None, "error": None})

    def destroy(self, request, *args, **kwargs):
        common_group_name = request.data.get('lecture_group_name')
        CommonLectureGroupService.delete_common_lecture_group(common_group_name)
        return Response({"success": True, "data": None, "error": None})
