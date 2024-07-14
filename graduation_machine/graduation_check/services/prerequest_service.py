from graduation_check.models import Prerequest, LectureGroup

class PrerequestService:
    @staticmethod
    def get_prerequests():
        try:
            return Prerequest.objects.all()
        except Exception as e:
            print(f"An unexpected error occurred while fetching prerequests: {str(e)}")
            return None

    @staticmethod
    def add_prerequest(lecture_group_id, prerequest_lecture_group_id):
        return Prerequest.objects.create(lecture_group_id=lecture_group_id, prerequest_lecture_group_id=prerequest_lecture_group_id)

    @staticmethod
    def add_prerequest(lecture_group_id, prerequest_lecture_group_id):
        try:
            # Ensure both lecture groups exist before creating a prerequest
            if not (LectureGroup.objects.filter(id=lecture_group_id).exists() and 
                    LectureGroup.objects.filter(id=prerequest_lecture_group_id).exists()):
                return {"status": "error", "message": "One or both lecture groups do not exist."}
            # Create the prerequest if both lecture groups exist
            Prerequest.objects.create(
                lecture_group_id=lecture_group_id, 
                prerequest_lecture_group_id=prerequest_lecture_group_id
            )
            return {"status": "success", "message": "Prerequest added successfully."}
        except Exception as e:
            # Handle any unexpected exceptions
            return {"status": "error", "message": f"An unexpected error occurred: {str(e)}"}