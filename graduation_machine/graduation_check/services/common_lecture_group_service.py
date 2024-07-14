from graduation_check.models import CommonLectureGroup

class CommonLectureGroupService:
    @staticmethod
    def get_all_common_lectures():
        return CommonLectureGroup.objects.all()
