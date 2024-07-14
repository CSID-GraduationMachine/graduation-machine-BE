from graduation_check.models import LectureGroup
from django.core.exceptions import ObjectDoesNotExist

class LectureGroupService:
    @staticmethod
    def get_common_lecture_groups(requirement_id):
        try:
            lecture_groups = LectureGroup.objects.filter(gr_id=requirement_id)
            if not lecture_groups.exists():
                return LectureGroup.objects.none()
            return lecture_groups
        except ObjectDoesNotExist:
            return LectureGroup.objects.none()
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            return None
