from ..models import Prerequest

class PrerequestService:
    @staticmethod
    def get_prerequests(lecture_group_id):
        try:
            return Prerequest.objects.filter(lecture_group_id=lecture_group_id)
        except Exception as e:
            print(f"An unexpected error occurred while fetching prerequests: {str(e)}")
            return None

    @staticmethod
    def create_prerequest(lecture_group_id, prerequest_year, prerequest_lecture_group_id):
        try:
            if Prerequest.objects.filter(lecture_group_id=lecture_group_id, year=prerequest_year, prerequest_lecture_group_id=prerequest_lecture_group_id).exists():
                return None # 이미 등록된 선이수면 None 반환
            return Prerequest.objects.create(lecture_group_id=lecture_group_id, year=prerequest_year, prerequest_lecture_group_id=prerequest_lecture_group_id)
        except Exception as e:
            print(f"An unexpected error occurred while creating prerequest: {str(e)}")
            return None
        
    @staticmethod
    def delete_prerequest(id):
        try:
            prerequest = Prerequest.objects.get(id=id)
            prerequest.delete()
            return True
        except Exception as e:
            print(f"An unexpected error occurred while deleting prerequest: {str(e)}")
            return None