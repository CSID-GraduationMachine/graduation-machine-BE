from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import GraduationRequirementsDetailSerializer
from .services.graduation_requirements_service import GraduationRequirementService
from .models import GraduationRequirements
from .serializers import LectureGroupSerializer
from .services.lecture_group_service import LectureGroupService
from .serializers import LectureSerializer
from .services.lecture_service import LectureService
from .services.prerequest_service import PrerequestService
from .serializers import PrerequestSerializer
from .services.prerequest_service import PrerequestService

class GraduationRequirementsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = GraduationRequirementsDetailSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        year = request.query_params.get('year')
        tech = request.query_params.get('tech')
        try:
            requirements = GraduationRequirementService.get_graduation_conditions(year, tech)
            details = GraduationRequirementService.get_graduation_requirements_details(requirements)
            response_data = {
                "entire_minimum_credit": requirements.total_minimum_credit,
                "details": GraduationRequirementsDetailSerializer(details, many=True).data
            }
            return Response({"success": True, "data": response_data, "error": None})
        except GraduationRequirements.DoesNotExist:
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
        prelecture_data = [{"pre_lecture_group_name": pre.prerequest_lecture_group.lecture_group_name, "pre_lecture_group_id": pre.prerequest_lecture_group.id} for pre in prelectures if pre.lecture_group.id == group_id]
        lecture_data = LectureSerializer(lectures, many=True).data
        return Response({"success": True, "data": [prelecture_data, lecture_data], "error": None})
    

class PrerequestViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = PrerequestSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        prerequests = PrerequestService.get_prerequests()
        return Response({"success": True, "data": PrerequestSerializer(prerequests, many=True).data, "error": None})