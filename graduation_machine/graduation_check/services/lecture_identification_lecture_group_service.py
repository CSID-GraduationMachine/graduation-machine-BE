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
        
    def create_lecture_identification_lecturegroup(lecture_group_id, type, keyword):
        try:
            lecture_identifications=None

            valid_types = ['none', 'name', 'code']
            if type not in valid_types:
                raise ValueError("Invalid type parameter")
            if type == 'none':
                lecture_identifications = LectureIdentification.objects.filter(id=keyword)
            elif type == 'name':
                lecture_identifications = LectureIdentification.objects.filter(name__icontains=keyword)
            elif type == 'code':
                lecture_identifications = LectureIdentification.objects.filter(code__icontains=keyword)

            # 이미 LectureIdentificationLectureGroup에 등록된 lecture_identification은 제외
            registered_lecture_identifications_id = LectureIdentificationLectureGroup.objects.filter(
                lecture_group_id=lecture_group_id
            ).values_list('lecture_identification_id', flat=True)
            lecture_identifications = lecture_identifications.exclude(id__in=registered_lecture_identifications_id)

            lecture_group = LectureGroup.objects.get(id=lecture_group_id)
            for lecture_identification in lecture_identifications:
                LectureIdentificationLectureGroup.objects.create(lecture_group=lecture_group, lecture_identification=lecture_identification)
            return True
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

