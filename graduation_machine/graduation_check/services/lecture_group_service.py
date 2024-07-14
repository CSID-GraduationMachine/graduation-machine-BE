from graduation_check.models import LectureGroup

class LectureGroupService:
    @staticmethod
    def get_common_lecture_groups(requirement_id):
        return LectureGroup.objects.filter(gr__id=requirement_id)
