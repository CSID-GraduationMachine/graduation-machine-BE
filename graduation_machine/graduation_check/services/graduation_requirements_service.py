from graduation_check.models import GraduationRequirements, GraduationRequirementsDetail

class GraduationRequirementService:
    @staticmethod
    def get_graduation_conditions(year, tech):
        return GraduationRequirements.objects.get(year=year, tech=tech)

    @staticmethod
    def get_graduation_requirements_details(graduation_requirement):
        return GraduationRequirementsDetail.objects.filter(gr=graduation_requirement)
