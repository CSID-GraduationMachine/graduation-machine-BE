from graduation_check.models import CommonLectureGroup

class CommonLectureGroupService:
    @staticmethod
    def get_all_common_lectures():
        try:
            commonLectureGroup = CommonLectureGroup.objects.all()
            return commonLectureGroup
        except CommonLectureGroup.DoesNotExist:
            return CommonLectureGroup.objects.none()

    @staticmethod
    def create_common_lecture_group(lecture_ids, common_group_name):
        try: 
           for lecture_id in lecture_ids:
              commonLectureGroup = CommonLectureGroup.objects.create(lecture_id=lecture_id, common_group_name=common_group_name)
              return commonLectureGroup
        except(ValueError, TypeError):
            return None
        

    @staticmethod
    def delete_common_lecture_group(group_id):
        try:
            group = CommonLectureGroup.objects.get(id=group_id)
            group.delete()
            return True
        except CommonLectureGroup.DoesNotExist:
            return False
