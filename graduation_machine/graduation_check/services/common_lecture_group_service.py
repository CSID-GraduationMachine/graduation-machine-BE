from graduation_check.models import CommonLectureGroup, CommonLectureGroupLecture

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
              commonLectureGroup = CommonLectureGroup.objects.create(common_group_name=common_group_name)
              CommonLectureGroupLecture.objects.create(lecture_id=lecture_id, common_lecture_group_id=commonLectureGroup.id)
              return True
        except(ValueError, TypeError):
            return None
        

    @staticmethod
    def delete_common_lecture_group(common_lecture_group_id):
        try:
            group = CommonLectureGroup.objects.get(id=common_lecture_group_id)
            CommonLectureGroupLecture.objects.filter(common_lecture_group_id=group.id).delete()
            group.delete()
            return True
        except CommonLectureGroup.DoesNotExist:
            return False
