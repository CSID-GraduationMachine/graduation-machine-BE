from graduation_check.models import Lecture
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
