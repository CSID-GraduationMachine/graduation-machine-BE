from .utils.graduation_check_util import GraduationCheckUtil
from ..models import LectureGroup, GraduationRequirements, GraduationRequirementsDetail, Lecture, LectureLectureGroup, Prerequest, CommonLectureGroup
from rest_framework.response import Response

class GraduationCheckService:
    def check_graduation(self, year, tech, excel_file):
        # data
        data = {}
        
        graduation_requirements = GraduationRequirements.objects.get(year = year, tech = tech)

        user_lectures = GraduationCheckUtil.read_excel(excel_file) # year, season, code

        # 1. 총 이수 최소 학점 확인
        total_credit = 0 
        
        for user_lecture in user_lectures:
            total_credit += user_lecture.credit
        graduation_minimum_total_credit = graduation_requirements.total_minimum_credit
        if total_credit < graduation_minimum_total_credit:
            data['total_credit_check_message'] = f"{total_credit}/{graduation_minimum_total_credit}"
            data['total_credit_check_value'] = False
        else:
            data['total_credit_check_message'] = f"{total_credit}/{graduation_minimum_total_credit}"
            data['total_credit_check_value'] = True
        
        # 2. 필수 강의 수강 여부 확인
        graduation_requirements_details = GraduationRequirementsDetail.objects.filter(gr = graduation_requirements) # 2020학번 심화과정 졸업 요건들 중
        for graduation_requirements_detail in graduation_requirements_details: # 각각의 졸업 요건 안에,
            mandatory_lecture_group_list = LectureGroup.objects.filter(grd = graduation_requirements_detail, is_mandatory = True)
            result_list = [{lecture_group.lecture_group_name: False} for lecture_group in mandatory_lecture_group_list] # 각각의 필수 강의 그룹에 대해 False로 초기화된 리스트 생성
            for mandatory_lecture_group in mandatory_lecture_group_list: # 속해있는 필수 강의 그룹에 대해
                mandatory_lecture_group_lectures = mandatory_lecture_group_lectures = LectureLectureGroup.objects.filter(lecture_group=mandatory_lecture_group).select_related('lecture') # 해당 필수 강의 그룹에 실제 맵핑되는 강의들을 mandatory_lecture_group_lectures에 저장
                for mandatory_lecture_group_lecture in mandatory_lecture_group_lectures: # 각각의 강의 하나하나마다 
                    mandatory_lecture = Lecture.objects.get(id = mandatory_lecture_group_lecture.lecture.id) # 사용자의 수강 강의 목록에 해당 강의가 있는지 확인
                    if mandatory_lecture in user_lectures: # 있다면
                        result_list[mandatory_lecture_group_list.index(mandatory_lecture_group)][mandatory_lecture_group.lecture_group_name] = True # 해당 필수 강의 그룹에 대해 True로 변경
                        break # 다음 필수 강의 그룹으로 넘어감
        data['mandatory_lecture_group_list'] = result_list

        # 3. 선수과목 수강 여부 확인
        for user_lecture in user_lectures:
            lecture = Lecture.objects.get(year = user_lecture.year, season = user_lecture.season, code = user_lecture.code)
            lecture_lecture_group = LectureLectureGroup.objects.get(lecture = lecture)
            lecture_group = LectureGroup.objects.get(id = lecture_lecture_group.lecture_group.id)
            prerequests = Prerequest.objects.filter(lecture_group = lecture_group)
            result_list = [{prerequest.prerequest_lecture_group.lecture_group_name: False} for prerequest in prerequests]
            for prerequest in prerequests:
                prerequest_lecture_group_lectures = LectureLectureGroup.objects.filter(lecture_group = prerequest.prerequest_lecture_group)
                for prerequest_lecture_group_lecture in prerequest_lecture_group_lectures:
                    prerequest_lecture = Lecture.objects.get(id = prerequest_lecture_group_lecture.lecture.id)
                    if prerequest_lecture in user_lectures:
                        result_list[prerequests.index(prerequest)][prerequest.prerequest_lecture_group.lecture_group_name] = True
                        break
            data[f"{lecture.code}_prerequest"] = result_list

        # 4. 각각의 졸업 요건 만족 여부 확인
        graduation_requirements_details = GraduationRequirementsDetail.objects.filter(gr = graduation_requirements)
        for graduation_requirements_detail in graduation_requirements_details:
            satisfying_credit = 0
            for user_lecture in user_lectures:
                lecture = Lecture.objects.get(year = user_lecture.year, season = user_lecture.season, code = user_lecture.code)
                lecture_lecture_group = LectureLectureGroup.objects.get(lecture = lecture)
                lecture_group = LectureGroup.objects.get(id = lecture_lecture_group.lecture_group.id)
                if lecture_group.id == graduation_requirements_detail.id:
                    satisfying_credit += user_lecture.credit
            if satisfying_credit < graduation_requirements_detail.minimum_credit:
                data[f"{graduation_requirements_detail.requirements_name}_message"] = f"{satisfying_credit}/{graduation_requirements_detail.minimum_credit}"
                data[f"{graduation_requirements_detail.requirements_name}_value"] = False
            else:
                data[f"{graduation_requirements_detail.requirements_name}_message"] = f"{satisfying_credit}/{graduation_requirements_detail.minimum_credit}"
                data[f"{graduation_requirements_detail.requirements_name}_value"] = True
        
        # 결과 JSON 반환
        return Response(data)


            
    
