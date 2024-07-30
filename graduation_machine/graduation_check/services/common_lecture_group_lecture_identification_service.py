from ..models import CommonLectureGroup, CommonLectureGroupLectureIdentification, LectureIdentification
from django.db.models import F
class CommonLectureGroupLectureIdentificationService:

    def get_lectures(common_lecture_group_id, orderby='year', sorttype='asc'):
        try:
            valid_order_fields = ['year', 'name', 'code']
            if orderby not in valid_order_fields:
                raise ValueError("Invalid orderby parameter")

            order_prefix = '-' if sorttype == 'desc' else ''

            lectures = CommonLectureGroupLectureIdentification.objects.filter(
                common_lecture_group=common_lecture_group_id
            ).annotate(
                sorted_year=F('lecture_identification__year'),
                sorted_season=F('lecture_identification__season'),
                sorted_name=F('lecture_identification__name'),
                sorted_code=F('lecture_identification__code')
            )

            if orderby == 'year':
                lectures = lectures.order_by(
                    f"{order_prefix}sorted_year", f"{order_prefix}sorted_season"
                )
            elif orderby == 'name':
                lectures = lectures.order_by(f"{order_prefix}sorted_name")
            elif orderby == 'code':
                lectures = lectures.order_by(f"{order_prefix}sorted_code")

            return lectures
        except Exception as e:
            print(f"An unexpected error occurred while fetching lectures: {str(e)}")
            return None
            
    def create_common_lecture_group_lecture_identification(common_lecture_group_id, type, keyword):
        try:
            lecture_identifications=None

            valid_types = ['none', 'name', 'code']
            if type not in valid_types:
                raise ValueError("Invalid type parameter")
            if type == 'none':
                lecture_identifications = LectureIdentification.objects.get(id=keyword)
            elif type == 'name':
                lecture_identifications = LectureIdentification.objects.filter(name__icontains=keyword)
            elif type == 'code':
                lecture_identifications = LectureIdentification.objects.filter(code__icontains=keyword)

            # 이미 CommonLectureGroupLectureIdentification에 등록된 lecture_identification은 제외
            registered_lecture_identifications_id = CommonLectureGroupLectureIdentification.objects.filter(
                common_lecture_group_id=common_lecture_group_id
            ).values_list('lecture_identification_id', flat=True)
            lecture_identifications = lecture_identifications.exclude(id__in=registered_lecture_identifications_id)

            common_lecture_group = CommonLectureGroup.objects.get(id=common_lecture_group_id)
            for lecture_identification in lecture_identifications:
                CommonLectureGroupLectureIdentification.objects.create(common_lecture_group=common_lecture_group, lecture_identification=lecture_identification)
            return True
        except Exception as e:
            print(f"An unexpected error occurred while creating common lecture group lecture identification: {str(e)}")
            return None
            
    def delete_common_lecture_group_lecture_identification(common_lecture_group_lecture_identification_id):
        try:
            common_lecture_group_lecture_identification = CommonLectureGroupLectureIdentification.objects.filter(id= common_lecture_group_lecture_identification_id)
            common_lecture_group_lecture_identification.delete()
            return True
        except Exception as e:
            print(f"An unexpected error occurred while deleting common lecture group lecture identification: {str(e)}")
            return None