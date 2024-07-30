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
            
    def create_common_lecture_group_lecture_identification(common_lecture_group_id, lecture_identification_id):
        try:
            lecture_identification = LectureIdentification.objects.get(id=lecture_identification_id)
            common_lecture_group = CommonLectureGroup.objects.get(id=common_lecture_group_id)
            return CommonLectureGroupLectureIdentification.objects.create(common_lecture_group = common_lecture_group, lecture_identification = lecture_identification)
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