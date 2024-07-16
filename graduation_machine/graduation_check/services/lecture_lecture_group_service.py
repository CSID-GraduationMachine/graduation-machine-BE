from graduation_check.models import LectureLectureGroup, LectureGroup, Lecture

class LectureLectureGroupService:
    
    def get_lecture_lecturegroups(lecture_group_id):
        try:
            return LectureLectureGroup.objects.filter(lecture_group=lecture_group_id)
        except Exception as e:
            print(f"An unexpected error occurred while fetching lectures: {str(e)}")
            return None
        
    def create_lecture_lecturegroup(lecture_group_id, lecture_id):
        try:
            lecture = Lecture.objects.get(id=lecture_id)
            lecture_group = LectureGroup.objects.get(id=lecture_group_id)
            return LectureLectureGroup.objects.create(lecture_group=lecture_group,lecture=lecture)
        except Exception as e:
            print(f"An unexpected error occurred while creating lecture lecturegroup: {str(e)}")
            return None
        
    def delete_lecture_lecturegroup(lecture_lecturegroups_id):
        try:
            lecture_lecturegroup = LectureLectureGroup.objects.filter(id=lecture_lecturegroups_id)
            lecture_lecturegroup.delete()
            return True
        except Exception as e:
            print(f"An unexpected error occurred while deleting lecture lecturegroup: {str(e)}")
            return None

