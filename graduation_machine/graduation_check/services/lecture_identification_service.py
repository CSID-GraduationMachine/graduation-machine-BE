from ..models import LectureIdentification
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status

class LectureIdentificationService:

    @staticmethod
    def get_lecture_identifications(orderby, sorttype):
        valid_order_fields = ['year', 'name', 'code']
        if orderby not in valid_order_fields:
            raise ValueError("Invalid orderby parameter")

        if sorttype == 'desc':
            orderby = '-' + orderby
        if orderby == 'year': # year을 기준으로 정렬할 때, season도 기준으로 정렬
            lecture_identifications = LectureIdentification.objects.order_by(orderby, 'season')
        else:
            lecture_identifications = LectureIdentification.objects.order_by(orderby)
        return list(lecture_identifications.values())
        
    @staticmethod
    def get_lecture_identification_by_id(lecture_identification_id):
        try:
            return LectureIdentification.objects.get(id=lecture_identification_id)
        except ObjectDoesNotExist:
            return None
        except Exception as e:
            print(f"An unexpected error occurred while fetching lecture identification: {str(e)}")
            return None