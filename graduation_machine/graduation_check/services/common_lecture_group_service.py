from graduation_check.models import CommonLectureGroup

class CommonLectureGroupService:
    @staticmethod
    def get_all_common_lectures():
        return CommonLectureGroup.objects.all()
    
    @staticmethod
    def create_common_lecture_group(lecture_ids, common_group_name):
        for lecture_id in lecture_ids:
            CommonLectureGroup.objects.create(lecture_id=lecture_id, common_group_name=common_group_name)
        return True
    
    @staticmethod
    def delete_common_lecture_group(common_group_name):
        CommonLectureGroup.objects.filter(common_group_name=common_group_name).delete()
        return True
