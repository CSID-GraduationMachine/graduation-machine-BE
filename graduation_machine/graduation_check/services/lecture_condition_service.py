from ..models import Condition, LectureCondition, LectureGroup, LectureIdentificationLectureGroup, Prerequest
from django.shortcuts import get_object_or_404

class LectureConditionService:

    @staticmethod
    def get_lecture_conditions(condition_id):
        try:
            condition = get_object_or_404(Condition, pk=condition_id)
            return LectureCondition.objects.filter(condition=condition)
        except LectureCondition.DoesNotExist:
            return None
    
    @staticmethod
    def create_lecture_condition(condition_id, lecture_condition_name, minimum_credit):
        try:
            condition = get_object_or_404(Condition, pk=condition_id)
            return LectureCondition.objects.create(
                condition=condition,
                condition_name=lecture_condition_name,
                minimum_credit=minimum_credit
            )
        except Exception as e:
            print(f"An unexpected error occurred while creating lecture conditions: {str(e)}")
            return None

    @staticmethod
    def update_lecture_condition(lecture_condition_id, lecture_condition_name, minimum_credit):
        try:
            lecture_condition = LectureCondition.objects.get(id = lecture_condition_id)
            lecture_condition.minimum_credit = minimum_credit
            lecture_condition.condition_name = lecture_condition_name
            lecture_condition.save()
            return lecture_condition
        except LectureCondition.DoesNotExist:
            return None
        except Exception as e:
            print(f"An unexpected error occurred while updating lecture conditions: {str(e)}")
            return None
        
    @staticmethod
    def delete_lecture_condition(lecture_condition_id):
        try:
            lecture_condition = LectureCondition.objects.get(id=lecture_condition_id)
            lecture_group = LectureGroup.objects.filter(lecture_condition=lecture_condition)
            LectureIdentificationLectureGroup.objects.filter(lecture_group__in=lecture_group).delete()
            Prerequest.objects.filter(lecture_group__in=lecture_group).delete()
            lecture_group.delete()
            lecture_condition.delete()
            return True
        except LectureCondition.DoesNotExist:
            return False
        except Exception as e:
            print(f"An unexpected error occurred while deleting lecture conditions: {str(e)}")
            return None