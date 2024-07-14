from graduation_check.models import Lecture

class LectureService:
    @staticmethod
    def get_common_lecture_descriptions(group_id):
        return Lecture.objects.filter(lecture_groups__id=group_id)
