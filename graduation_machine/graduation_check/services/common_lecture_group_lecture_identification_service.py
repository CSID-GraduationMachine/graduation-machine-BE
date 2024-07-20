from ..models import CommonLectureGroup, CommonLectureGroupLectureIdentification, LectureIdentification
class CommonLectureGroupLectureIdentificationService:
        
        def get_lectures(common_lecture_group_id):
            try:
                return CommonLectureGroupLectureIdentification.objects.filter(common_lecture_group = common_lecture_group_id)
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