from graduation_check.models import Prerequest

class PrerequestService:
    @staticmethod
    def get_prerequests():
        return Prerequest.objects.all()
