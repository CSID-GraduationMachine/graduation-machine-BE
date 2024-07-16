from graduation_check.models import CommonLectureGroup, CommonLectureGroupLecture, Lecture

class CommonLectureGroupLectureService:
        
        def get_lectures(common_lecture_group_id):
            try:
                return CommonLectureGroupLecture.objects.filter(common_lecture_group=common_lecture_group_id)
            except Exception as e:
                print(f"An unexpected error occurred while fetching lectures: {str(e)}")
                return None
            
        def create_common_lecture_group_lecture(common_lecture_group_id, lecture_id):
            try:
                lecture = Lecture.objects.get(id=lecture_id)
                common_lecture_group = CommonLectureGroup.objects.get(id=common_lecture_group_id)
                return CommonLectureGroupLecture.objects.create(common_lecture_group=common_lecture_group,lecture=lecture)
            except Exception as e:
                print(f"An unexpected error occurred while creating common lecture group lecture: {str(e)}")
                return None
            
        def delete_common_lecture_group_lecture(common_lecture_group_lecture_id):
            try:
                common_lecture_group_lecture = CommonLectureGroupLecture.objects.filter(id= common_lecture_group_lecture_id)
                common_lecture_group_lecture.delete()
                return True
            except Exception as e:
                print(f"An unexpected error occurred while deleting common lecture group lecture: {str(e)}")
                return None