from ..models import LectureIdentification, LectureGroup, LectureIdentificationLectureGroup, CommonLectureGroup, CommonLectureGroupLectureIdentification
from django.core.exceptions import ObjectDoesNotExist

class LectureIdentificationService:

    @staticmethod
    def get_lecture_identifications():
        try:
            return LectureIdentification.objects.all()
        except Exception as e:
            print(f"An unexpected error occurred while fetching lecture identifications: {str(e)}")
            return None
        
    @staticmethod
    def get_lecture_identification_by_id(lecture_identification_id):
        try:
            return LectureIdentification.objects.get(id=lecture_identification_id)
        except ObjectDoesNotExist:
            return None
        except Exception as e:
            print(f"An unexpected error occurred while fetching lecture identification: {str(e)}")
            return None