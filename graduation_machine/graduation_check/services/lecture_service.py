from graduation_check.models import Lecture, LectureGroup, LectureLectureGroup, CommonLectureGroup, CommonLectureGroupLecture
from django.core.exceptions import ObjectDoesNotExist

class LectureService:
    @staticmethod
    def get_common_lecture_descriptions(group_id):
        try:
            lecture_lecture_group = LectureLectureGroup.objects.get(lecture_group__id = group_id)
            lectures = Lecture.objects.filter(id=lecture_lecture_group.lecture_id)
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
        
    @staticmethod
    def delete_lecture_on_lecture_lecture_group(lecture_id, lecture_group_id):
        try:
            lecture_lecture_group = LectureLectureGroup.objects.get(lecture_id=lecture_id, lecture_group_id=lecture_group_id)
            lecture_lecture_group.delete()
            return True
        except LectureLectureGroup.DoesNotExist:
            return False
        except Exception as e:
            print(f"An unexpected error occurred while deleting lecture on lecture group: {str(e)}")
            return None