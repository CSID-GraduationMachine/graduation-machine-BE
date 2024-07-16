from graduation_check.models import Lecture, LectureGroup, LectureLectureGroup, CommonLectureGroup, CommonLectureGroupLecture
from django.core.exceptions import ObjectDoesNotExist

class LectureService:

    @staticmethod
    def get_lectures():
        try:
            return Lecture.objects.all()
        except Exception as e:
            print(f"An unexpected error occurred while fetching lectures: {str(e)}")
            return None
        
    @staticmethod
    def get_lecture_by_id(lecture_id):
        try:
            return Lecture.objects.get(id=lecture_id)
        except ObjectDoesNotExist:
            return None
        except Exception as e:
            print(f"An unexpected error occurred while fetching lecture: {str(e)}")
            return None