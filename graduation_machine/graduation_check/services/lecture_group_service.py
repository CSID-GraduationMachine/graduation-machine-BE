from ..models import LectureGroup, Prerequest, LectureCondition
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

class LectureGroupService:
    @staticmethod
    def get_lecture_groups(lecture_condition_id):
        try:
            return LectureGroup.objects.filter(lecture_condition__id=lecture_condition_id).order_by('lecture_group_name')
        except Exception as e:
            print(f"An unexpected error occurred while fetching lecture groups: {str(e)}")
            return None
    @staticmethod
    def get_lecture_groups_for_add_prerequest(lecture_condition_id, lecture_group_id):
        try:
            # 선이수로 등록된 강의 그룹 ID 조회
            registered_lecture_groups_id = Prerequest.objects.filter(
                lecture_group_id=lecture_group_id
            ).values_list('prerequest_lecture_group_id', flat=True)

            condition = LectureCondition.objects.get(id=lecture_condition_id).condition

            # 현재 condition 상에서, 현재 강의 그룹과 선이수 강의 그룹을 제외한 강의 그룹을 조회
            available_groups = LectureGroup.objects.exclude(
                Q(lecture_condition__condition=condition) &
                (
                        Q(id=lecture_group_id) |
                        Q(id__in=registered_lecture_groups_id))
            ).order_by('lecture_group_name')
            return available_groups
        except Exception as e:
            print(f"An unexpected error occurred while fetching lecture groups for add prerequest: {str(e)}")
            return None

    @staticmethod
    def create_lecture_group(lecture_condition_id, lecture_group_name, is_essential):
        try:
            return LectureGroup.objects.create(lecture_condition_id=lecture_condition_id, lecture_group_name=lecture_group_name, is_essential=is_essential)
        except Exception as e:
            print(f"An unexpected error occurred while creating lecture group: {str(e)}")
            return None
    @staticmethod
    def update_lecture_group(lecture_group_id, lecture_group_name, is_essential):
        try:
            lecture_group = LectureGroup.objects.get(id=lecture_group_id)
            lecture_group.lecture_group_name = lecture_group_name
            lecture_group.is_essential = is_essential
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