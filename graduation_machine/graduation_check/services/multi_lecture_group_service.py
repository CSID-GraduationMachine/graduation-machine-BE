from ..models import MultiLectureGroup, LectureGroup
class MultiLectureGroupService:
    @staticmethod
    def create_multi_lecture_group(lecture_group_id):
        try:
            if LectureGroup.objects.get(id=lecture_group_id).multi_lecture_group is not None:
                raise ValueError("이미 등록된 다중 강의 그룹입니다.")
            else:
                multi_lecture_group = MultiLectureGroup.objects.create(minimum_credit=1, maximum_credit=1)
                lecture_group = LectureGroup.objects.get(id=lecture_group_id)
                lecture_group.multi_lecture_group = multi_lecture_group
                lecture_group.save()
        except Exception as e:
            print(f"An unexpected error occurred while creating multi lecture group: {str(e)}")

    def get_multi_lecture_groups(lecture_group_id):
        try:
            lecture_group = LectureGroup.objects.get(id=lecture_group_id)
            return MultiLectureGroup.objects.filter(id=lecture_group.multi_lecture_group.id)
        except Exception as e:
            print(f"An unexpected error occurred while fetching multi lecture groups: {str(e)}")
            return None

    @staticmethod
    def update_multi_lecture_group(multi_lecture_group_id, minimum_number, maximum_number):
        try:
            multi_lecture_group = MultiLectureGroup.objects.get(id=multi_lecture_group_id)
            multi_lecture_group.minimum_number = minimum_number
            multi_lecture_group.maximum_number = maximum_number
            multi_lecture_group.save()
        except Exception as e:
            print(f"An unexpected error occurred while updating multi lecture group: {str(e)}")

    @staticmethod
    def delete_multi_lecture_group(multi_lecture_group_id):
        try:
            multi_lecture_group = MultiLectureGroup.objects.get(id=multi_lecture_group_id)
            multi_lecture_group.delete()
        except Exception as e:
            print(f"An unexpected error occurred while deleting multi lecture group: {str(e)}")