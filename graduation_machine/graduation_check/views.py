from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import GraduationRequirementsDetailSerializer
from .services.graduation_requirements_service import GraduationRequirementService
from .models import GraduationRequirements
from .serializers import LectureGroupSerializer
from .services.lecture_group_service import LectureGroupService

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
