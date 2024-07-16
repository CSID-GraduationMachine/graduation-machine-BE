from graduation_check.models import GraduationRequirementsDetail
from graduation_check.models import GraduationRequirements
from graduation_check.models import LectureGroup
from graduation_check.models import LectureLectureGroup
from graduation_check.models import Prerequest
from django.shortcuts import get_object_or_404

class GraduationRequirementDetailService:

    @staticmethod
    def get_graduation_requirements_details(requirement_id):
        try:
            graduation_requirement = get_object_or_404(GraduationRequirements, pk=requirement_id)
            return GraduationRequirementsDetail.objects.filter(gr=graduation_requirement)
        except GraduationRequirements.DoesNotExist:
            return None
    
    @staticmethod
    def create_graduation_conditions(requirement_id, requirements_name, minimum_credit):
        try:
            graduation_requirement = get_object_or_404(GraduationRequirements, pk=requirement_id)
            return GraduationRequirementsDetail.objects.create(
                gr=graduation_requirement,
                requirements_name=requirements_name,
                minimum_credit=minimum_credit
            )
        except Exception as e:
            print(f"An unexpected error occurred while creating graduation conditions: {str(e)}")
            return None

    @staticmethod
    def update_graduation_conditions(requirement_detail_id, requirement_name, minimum_credit):
        try:
            requirement = GraduationRequirementsDetail.objects.get(id=requirement_detail_id)
            requirement.minimum_credit = minimum_credit
            requirement.requirements_name = requirement_name
            requirement.save()
            return requirement
        except GraduationRequirements.DoesNotExist:
            return None
        except Exception as e:
            print(f"An unexpected error occurred while updating graduation conditions: {str(e)}")
            return None
        
    @staticmethod
    def delete_graduation_conditions(requirement_id):
        try:
            requirement = GraduationRequirementsDetail.objects.get(id=requirement_id)
            lecture_group = LectureGroup.objects.filter(grd=requirement)
            LectureLectureGroup.objects.filter(lecture_group__in=lecture_group).delete()
            Prerequest.objects.filter(lecture_group__in=lecture_group).delete()
            lecture_group.delete()
            requirement.delete()
            return True
        except GraduationRequirements.DoesNotExist:
            return False
        except Exception as e:
            print(f"An unexpected error occurred while deleting graduation conditions: {str(e)}")
            return None