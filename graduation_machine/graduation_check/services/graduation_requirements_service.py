from graduation_check.models import GraduationRequirements
from django.shortcuts import get_object_or_404

class GraduationRequirementService:
    @staticmethod
    def get_total_minimum_credit(requirement_id):
        try:
            return get_object_or_404(GraduationRequirements, pk=requirement_id).total_minimum_credit
        except GraduationRequirements.DoesNotExist:
            return None
    @staticmethod
    def get_graduation_requirements():
        try:
            return GraduationRequirements.objects.all()
        except Exception as e:
            print(f"An unexpected error occurred while fetching graduation requirements: {str(e)}")
            return None

    @staticmethod
    def create_graduation_requirements(year, tech, total_minimum_credit):
        return GraduationRequirements.objects.create(year=year, tech=tech, total_minimum_credit=total_minimum_credit)

    @staticmethod
    def update_graduation_requirements(requirement_id, year, tech, total_minimum_credit):
        try:
            requirement = GraduationRequirements.objects.get(id=requirement_id)
            requirement.year = year
            requirement.tech = tech
            requirement.total_minimum_credit = total_minimum_credit
            requirement.save()
            return requirement
        except GraduationRequirements.DoesNotExist:
            return None
        except Exception as e:
            print(f"An unexpected error occurred while updating graduation requirements: {str(e)}")
            return None

    @staticmethod
    def delete_graduation_requirements(requirement_id):
        try:
            requirement = GraduationRequirements.objects.get(id=requirement_id)
            requirement.delete()
            return True
        except GraduationRequirements.DoesNotExist:
            return False
        except Exception as e:
            print(f"An unexpected error occurred while deleting graduation requirements: {str(e)}")
            return None