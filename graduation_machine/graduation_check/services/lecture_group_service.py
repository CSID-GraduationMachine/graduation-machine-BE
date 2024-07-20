from ..models import LectureGroup
from django.core.exceptions import ObjectDoesNotExist

class LectureGroupService:
    @staticmethod
    def get_lecture_groups(lecture_condition_id):
        try:
            return LectureGroup.objects.filter(lecture_condition__id=lecture_condition_id)
        except Exception as e:
            print(f"An unexpected error occurred while fetching lecture groups: {str(e)}")
            return None
    @staticmethod
    def create_lecture_group(lecture_condition_id, lecture_group_name, is_essential):
        try:
            return LectureGroup.objects.create(lecture_condition_id=lecture_condition_id, lecture_group_name=lecture_group_name, is_essential=is_essential)
        except Exception as e:
            print(f"An unexpected error occurred while creating lecture group: {str(e)}")
            return None
    @staticmethod
    def update_lecture_group(lecture_group_id, lecture_group_name):
        try:
            lecture_group = LectureGroup.objects.get(id=lecture_group_id)
            lecture_group.lecture_group_name = lecture_group_name
            lecture_group.save()
            return lecture_group
        except ObjectDoesNotExist:
            return None
        except Exception as e:
            print(f"An unexpected error occurred while updating lecture group: {str(e)}")
            return None
    @staticmethod
    def delete_lecture_group(lecture_group_id):
        try:
            lecture_group = LectureGroup.objects.get(id=lecture_group_id)
            lecture_group.delete()
            return True
        except ObjectDoesNotExist:
            return False
        except Exception as e:
            print(f"An unexpected error occurred while deleting lecture group: {str(e)}")
            return None