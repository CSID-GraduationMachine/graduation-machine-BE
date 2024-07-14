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
        
    @staticmethod
    def update_graduation_conditions(requirement_id, data):
        try:
            requirement = GraduationRequirementsDetail.objects.get(id=requirement_id)
            requirement.minimum_credit = data.get('minimum_credit')
            requirement.requirements_name = data.get('requirement_name')
            requirement.save()
            return requirement
        except GraduationRequirements.DoesNotExist:
            return None
        except Exception as e:
            print(f"An unexpected error occurred while updating graduation conditions: {str(e)}")
            return None