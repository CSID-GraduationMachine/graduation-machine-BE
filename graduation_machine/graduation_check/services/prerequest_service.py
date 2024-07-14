from graduation_check.models import Prerequest

class PrerequestService:
    @staticmethod
    def get_prerequests():
        return Prerequest.objects.all()

    @staticmethod
    def add_prerequest(lecture_group_id, prerequest_lecture_group_id):
        return Prerequest.objects.create(lecture_group_id=lecture_group_id, prerequest_lecture_group_id=prerequest_lecture_group_id)
