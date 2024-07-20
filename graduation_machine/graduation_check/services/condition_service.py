from ..models import Condition
from django.shortcuts import get_object_or_404

class ConditionService:
    @staticmethod
    def get_total_minimum_credit(condition_id):
        try:
            return get_object_or_404(Condition, pk=condition_id).total_minimum_credit
        except Condition.DoesNotExist:
            return None
    @staticmethod
    def get_conditions():
        try:
            return Condition.objects.all()
        except Exception as e:
            print(f"An unexpected error occurred while fetching conditions: {str(e)}")
            return None

    @staticmethod
    def create_condition(year, tech, total_minimum_credit):
        return Condition.objects.create(year=year, tech=tech, total_minimum_credit=total_minimum_credit)

    @staticmethod
    def update_condition(condition_id, year, tech, total_minimum_credit):
        try:
            condition = Condition.objects.get(id=condition_id)
            condition.year = year
            condition.tech = tech
            condition.total_minimum_credit = total_minimum_credit
            condition.save()
            return condition
        except Condition.DoesNotExist:
            return None
        except Exception as e:
            print(f"An unexpected error occurred while updating conditions: {str(e)}")
            return None

    @staticmethod
    def delete_condition(condition_id):
        try:
            condition = Condition.objects.get(id=condition_id)
            condition.delete()
            return True
        except Condition.DoesNotExist:
            return False
        except Exception as e:
            print(f"An unexpected error occurred while deleting conditions: {str(e)}")
            return None