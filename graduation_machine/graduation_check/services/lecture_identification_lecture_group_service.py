from ..models import LectureIdentificationLectureGroup, LectureGroup, LectureIdentification
from django.db.models import F
class LectureIdentificationLectureGroupService:

    def get_lecture_identification_lecturegroups(lecture_group_id, orderby='year', sorttype='asc'):
        try:
            valid_order_fields = ['year', 'name', 'code']
            if orderby not in valid_order_fields:
                raise ValueError("Invalid orderby parameter")

            order_prefix = '-' if sorttype == 'desc' else ''

            lecture_identifications = LectureIdentificationLectureGroup.objects.filter(
                lecture_group=lecture_group_id
            ).annotate(
                sorted_year=F('lecture_identification__year'),
                sorted_season=F('lecture_identification__season'),
                sorted_name=F('lecture_identification__name'),
                sorted_code=F('lecture_identification__code')
            )

            if orderby == 'year':
                lecture_identifications = lecture_identifications.order_by(
                    f"{order_prefix}sorted_year", f"{order_prefix}sorted_season"
                )
            elif orderby == 'name':
                lecture_identifications = lecture_identifications.order_by(f"{order_prefix}sorted_name")
            elif orderby == 'code':
                lecture_identifications = lecture_identifications.order_by(f"{order_prefix}sorted_code")

            return lecture_identifications
        except Exception as e:
            print(f"An unexpected error occurred while fetching lectures: {str(e)}")
            return None
        
    def create_lecture_identification_lecturegroup(lecture_group_id, lecture_identification_id):
        try:
            lecture_identification = LectureIdentification.objects.get(id=lecture_identification_id)
            lecture_group = LectureGroup.objects.get(id=lecture_group_id)
            return LectureIdentificationLectureGroup.objects.create(lecture_group=lecture_group,lecture_identification=lecture_identification)
        except Exception as e:
            print(f"An unexpected error occurred while creating lecture identification lecturegroup: {str(e)}")
            return None
        
    def delete_lecture_identification_lecturegroup(lecture_identification_lecture_id):
        try:
            lecture_identification_lecturegroup = LectureIdentificationLectureGroup.objects.filter(id=lecture_identification_lecture_id)
            lecture_identification_lecturegroup.delete()
            return True
        except Exception as e:
            print(f"An unexpected error occurred while deleting lecture identification lecturegroup: {str(e)}")
            return None

