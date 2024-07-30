from ..models import CommonLectureGroup, CommonLectureGroupLectureIdentification

class CommonLectureGroupService:
    @staticmethod
    def get_all_common_lectures():
        try:
            common_lecture_group = CommonLectureGroup.objects.all().order_by('common_group_name')
            return common_lecture_group
        except CommonLectureGroup.DoesNotExist:
            return CommonLectureGroup.objects.none()

    @staticmethod
    def create_common_lecture_group(common_group_name):
        try: 
            CommonLectureGroup.objects.create(common_group_name=common_group_name)
            return True
        except(ValueError, TypeError):
            return None
        
    @staticmethod
    def update_common_lecture_group(common_lecture_group_id, common_group_name):
        try:
            group = CommonLectureGroup.objects.get(id=common_lecture_group_id)
            group.common_group_name = common_group_name
            group.save()
            return True
        except CommonLectureGroup.DoesNotExist:
            return None
        

    @staticmethod
    def delete_common_lecture_group(common_lecture_group_id):
        try:
            group = CommonLectureGroup.objects.get(id=common_lecture_group_id)
            CommonLectureGroupLectureIdentification.objects.filter(common_lecture_group_id=group.id).delete()
            group.delete()
            return True
        except CommonLectureGroup.DoesNotExist:
            return False
