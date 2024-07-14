from .utils.graduation_check_util import GraduationCheckUtil
from ..models import LectureGroup, GraduationRequirements, GraduationRequirementsDetail, Lecture, LectureLectureGroup, Prerequest

class GraduationCheckService:
    def check_graduation(self, year, tech, excel_file):
        # data
        data = {
            'graduation_requirements_detail_check': [],
            'mandatory_lecture_group_check': [],
            'total_credit_check': {},
            'prerequest_check': [],
            'grade_point_check': {}
        }
        
        graduation_requirements = GraduationRequirements.objects.get(year = year, tech = tech)

        user_lectures = GraduationCheckUtil.read_report_card(excel_file) # year, season, code, credit, grade
        user_lectures_codes = [user_lecture['code'] for user_lecture in user_lectures]

        # 1. 총 이수 최소 학점 확인
        total_credit = 0 
        
        for user_lecture in user_lectures:
            if(user_lecture['grade'] == 'F'):
                continue
            total_credit += user_lecture['credit']
        graduation_minimum_total_credit = graduation_requirements.total_minimum_credit
        if total_credit < graduation_minimum_total_credit:
            data['total_credit_check']['progress_ratio'] = f"{total_credit}/{graduation_minimum_total_credit}"
            data['total_credit_check']['check_value'] = False
        else:
            data['total_credit_check']['progress_ratio'] = f"{total_credit}/{graduation_minimum_total_credit}" 
            data['total_credit_check']['check_value'] = True
        
        # 2. 필수 강의 수강 여부 확인
        graduation_requirements_details = GraduationRequirementsDetail.objects.filter(gr = graduation_requirements) # 2020학번 심화과정 졸업 요건들 중
        for graduation_requirements_detail in graduation_requirements_details: # 각각의 졸업 요건 안에,
            mandatory_lecture_group_list = list(LectureGroup.objects.filter(grd = graduation_requirements_detail, is_mandatory = True))
            result_list = [{lecture_group.lecture_group_name: False} for lecture_group in mandatory_lecture_group_list] # 각각의 필수 강의 그룹에 대해 False로 초기화된 리스트 생성
            for mandatory_lecture_group in mandatory_lecture_group_list: # 속해있는 필수 강의 그룹에 대해
                mandatory_lecture_group_lectures = LectureLectureGroup.objects.filter(lecture_group=mandatory_lecture_group).select_related('lecture') # 해당 필수 강의 그룹에 실제 맵핑되는 강의들을 mandatory_lecture_group_lectures에 저장
                for mandatory_lecture_group_lecture in mandatory_lecture_group_lectures: # 각각의 강의 하나하나마다 
                    mandatory_lecture = Lecture.objects.get(id = mandatory_lecture_group_lecture.lecture.id) # 사용자의 수강 강의 목록에 해당 강의가 있는지 확인
                    if mandatory_lecture.code in user_lectures_codes: # 있다면
                        result_list[mandatory_lecture_group_list.index(mandatory_lecture_group)][mandatory_lecture_group.lecture_group_name] = True # 해당 필수 강의 그룹에 대해 True로 변경
                        break # 다음 필수 강의 그룹으로 넘어감
        # result_list를 새로운 포맷으로 변환
        for result in result_list:
            for group_name, check_value in result.items():
                mandatory_status = {
                    "mandatory_lecture_group_name": group_name,
                    "check_value": check_value
                }
                data['mandatory_lecture_group_check'].append(mandatory_status)

        # 3. 선수과목 수강 여부 확인
        if Prerequest.objects.all().count() == 0:
            data['prerequest_check'].append({
                "prerequest_lecture_group_name": "선수과목 정보가 없습니다.",
                "check_value": True
            })
        else:
            for user_lecture in user_lectures:
                lecture = Lecture.objects.get(year = user_lecture['year'], season = user_lecture['season'], code = user_lecture['code'], credit = user_lecture['credit'])
                lecture_lecture_group = LectureLectureGroup.objects.get(lecture = lecture)
                lecture_group = LectureGroup.objects.get(id = lecture_lecture_group.lecture_group.id)
                prerequests = Prerequest.objects.filter(lecture_group = lecture_group)
                result_list = [{prerequest.prerequest_lecture_group.lecture_group_name: False} for prerequest in prerequests]
                for prerequest in prerequests:
                    prerequests_list = list(prerequests)
                    prerequest_lecture_group_lectures = LectureLectureGroup.objects.filter(lecture_group = prerequest.prerequest_lecture_group)
                    for prerequest_lecture_group_lecture in prerequest_lecture_group_lectures:
                        prerequest_lecture = Lecture.objects.get(id = prerequest_lecture_group_lecture.lecture.id)
                        if prerequest_lecture.code in user_lectures_codes:
                            result_list[prerequests_list.index(prerequest)][prerequest.prerequest_lecture_group.lecture_group_name] = True
                            break

                    for result in result_list:
                        for group_name, check_value in result.items():
                            prerequest_status = {
                                "prerequest_lecture_group_name": group_name,
                                "check_value": check_value
                            }
                            data['prerequest_check'].append(prerequest_status)

        # 4. 각각의 졸업 요건 만족 여부 확인
        graduation_requirements_details = GraduationRequirementsDetail.objects.filter(gr=graduation_requirements)
        for graduation_requirements_detail in graduation_requirements_details:
            satisfying_credit = 0
            for user_lecture in user_lectures:
                try:
                    lecture = Lecture.objects.get(year=user_lecture['year'], season=user_lecture['season'], code=user_lecture['code'], credit=user_lecture['credit'])
                    lecture_lecture_group = LectureLectureGroup.objects.get(lecture=lecture)
                except Lecture.DoesNotExist:
                    data[f"{user_lecture['code']}_missing"] = f"Lecture with year={user_lecture['year']}, season={user_lecture['season']}, code={user_lecture['code']}, credit={user_lecture['credit']} does not exist."
                    continue
                except LectureLectureGroup.DoesNotExist:
                    continue  # lecture_lecture_group이 없으면 다음 요소로 넘어감
                
                lecture_group = LectureGroup.objects.get(id=lecture_lecture_group.lecture_group.id)
                if lecture_group.grd_id == graduation_requirements_detail.id:  # 비교 수정
                    satisfying_credit += user_lecture['credit']
            
            requirement_status = {
                "requirement_name": graduation_requirements_detail.requirements_name,
                "progress_ratio": f"{satisfying_credit}/{graduation_requirements_detail.minimum_credit}",
                "check_value": satisfying_credit >= graduation_requirements_detail.minimum_credit
            }
            data["graduation_requirements_detail_check"].append(requirement_status)


        # 5. 학점 평점 2.0 이상 확인
        user_lecture_score = 0.0
        user_total_credit = 0

        for user_lecture in user_lectures:
            if user_lecture['grade'] == 'A+':
                user_lecture_score += 4.5 * user_lecture['credit']
                user_total_credit += user_lecture['credit']
            elif user_lecture['grade'] == 'A0':
                user_lecture_score += 4.0 * user_lecture['credit']
                user_total_credit += user_lecture['credit']
            elif user_lecture['grade'] == 'B+':
                user_lecture_score += 3.5 * user_lecture['credit']
                user_total_credit += user_lecture['credit']
            elif user_lecture['grade'] == 'B0':
                user_lecture_score += 3.0 * user_lecture['credit']
                user_total_credit += user_lecture['credit']
            elif user_lecture['grade'] == 'C+':
                user_lecture_score += 2.5 * user_lecture['credit']
                user_total_credit += user_lecture['credit']
            elif user_lecture['grade'] == 'C0':
                user_lecture_score += 2.0 * user_lecture['credit']
                user_total_credit += user_lecture['credit']
            elif user_lecture['grade'] == 'D+':
                user_lecture_score += 1.5 * user_lecture['credit']
                user_total_credit += user_lecture['credit']
            elif user_lecture['grade'] == 'D0':
                user_lecture_score += 1.0 * user_lecture['credit']
                user_total_credit += user_lecture['credit']
            elif user_lecture['grade'] == 'F':
                user_lecture_score += 0.0 * user_lecture['credit']
                user_total_credit += user_lecture['credit']
            else:
                continue
        if user_lecture_score / total_credit < 2.0:
            data['grade_point_check']['progress_ratio'] = f"{user_lecture_score / user_total_credit}"   
            data['grade_point_check']['check_value'] = False
        else:
            data['grade_point_check']['progress_ratio'] = f"{user_lecture_score / user_total_credit}"   
            data['grade_point_check']['check_value'] = True
        # 결과 JSON 반환
        return data

    
