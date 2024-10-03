from ..models import LectureGroup, Prerequest, LectureCondition, MultiLectureGroup
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

            # 현재 condition 상에서, 현재 condition에 포함되어있지 않은 lecture group들을 제외 + 현재 강의 그룹과 선이수 강의 그룹을 제외한 강의 그룹을 조회
            available_groups = LectureGroup.objects.exclude(
                ~Q(lecture_condition__condition = condition) |
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
    def update_lecture_group(lecture_group_id, lecture_group_name, is_essential, is_multi_lecture, maximum_number, minimum_number):
        try:
            # LectureGroup 객체를 가져옴
            lecture_group = LectureGroup.objects.get(id=lecture_group_id)
            lecture_group.lecture_group_name = lecture_group_name
            lecture_group.is_essential = is_essential
            lecture_group.save()

            # 다중 강의 그룹 존재 여부 확인
            multi_lecture_group = MultiLectureGroup.objects.filter(id=lecture_group_id).first()

            if is_multi_lecture and multi_lecture_group is None: # 다중 강의 그룹이 없는데 true인 경우 생성
                multi_lecture_group = MultiLectureGroup.objects.create(id=lecture_group, minimum_number=minimum_number, maximum_number=maximum_number)
                lecture_group.multi_lecture_group = multi_lecture_group
                lecture_group.save()
            elif is_multi_lecture and multi_lecture_group is not None: # 다중강의 그룹이 있는데 true인 경우 수정
                multi_lecture_group.minimum_number = minimum_number
                multi_lecture_group.maximum_number = maximum_number
                multi_lecture_group.save()
            elif not is_multi_lecture and multi_lecture_group is not None: # 다중 강의 그룹이 있는데 false인 경우 삭제
                multi_lecture_group.delete()

        except LectureGroup.DoesNotExist:
            print(f"LectureGroup with id {lecture_group_id} does not exist.")
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