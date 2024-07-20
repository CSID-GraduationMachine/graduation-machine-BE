from ..models import LectureIdentificationLectureGroup, LectureGroup, LectureIdentification

class LectureIdentificationLectureGroupService:
    
    def get_lecture_identification_lecturegroups(lecture_group_id):
        try:
            return LectureIdentificationLectureGroup.objects.filter(lecture_group=lecture_group_id)
        except Exception as e:
            print(f"An unexpected error occurred while fetching lectures: {str(e)}")
            return None
        
    def create_lecture_identification_lecturegroup(lecture_group_id, lecture_identification_id):
        try:
            lecture_identification = LectureIdentification.objects.get(id=lecture_identification_id)
            lecture_group = LectureGroup.objects.get(id=lecture_group_id)
            return LectureIdentificationLectureGroup.objects.create(lecture_group=lecture_group,lecture_identification=lecture_identification)
        except Exception as e:
            print(f"An unexpected error occurred while creating lecture identification lecturegroup: {str(e)}")
            return None
        
    def delete_lecture_identification_lecturegroup(lecture_identification_lecture_id):
        try:
            lecture_identification_lecturegroup = LectureIdentificationLectureGroup.objects.filter(id=lecture_identification_lecture_id)
            lecture_identification_lecturegroup.delete()
            return True
        except Exception as e:
            print(f"An unexpected error occurred while deleting lecture identification lecturegroup: {str(e)}")
            return None

