from graduation_check.models import Lecture, CommonLectureGroup, CommonLectureGroupLecture
from django.core.exceptions import ObjectDoesNotExist

class LectureService:
    @staticmethod
    def get_common_lecture_descriptions(group_id):
        try:
            lectures = Lecture.objects.filter(lecture_groups__id=group_id)
            if not lectures.exists():
                return Lecture.objects.none()
            return lectures
        except ObjectDoesNotExist:
            return Lecture.objects.none()
        except Exception as e:
            print(f"An unexpected error occurred while fetching lectures: {str(e)}")
            return None
        
    @staticmethod
    def get_common_lectures(common_lecture_group_id):
        try:
            common_lecture_group = CommonLectureGroup.objects.get(id=common_lecture_group_id)
            common_lecture_group_lectures = CommonLectureGroupLecture.objects.filter(common_lecture_group_id=common_lecture_group.id)
            lectures = [lecture.lecture for lecture in common_lecture_group_lectures]
            return lectures
        except CommonLectureGroup.DoesNotExist:
            return CommonLectureGroup.objects.none()
        except Exception as e:
            print(f"An unexpected error occurred while fetching lectures: {str(e)}")
            return None