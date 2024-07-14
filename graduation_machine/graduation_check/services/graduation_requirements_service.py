from graduation_check.models import GraduationRequirements, GraduationRequirementsDetail
from django.shortcuts import get_object_or_404

class GraduationRequirementService:
    @staticmethod
    def get_graduation_conditions(year, tech):
        try:
            return GraduationRequirements.objects.get(year=year, tech=tech)
        except GraduationRequirements.DoesNotExist:
            return None

    @staticmethod
    def get_graduation_requirements_details(requirement_id):
        try:
            graduation_requirement = get_object_or_404(GraduationRequirements, pk=requirement_id)
            return GraduationRequirementsDetail.objects.filter(gr=graduation_requirement)
        except GraduationRequirements.DoesNotExist:
            return None