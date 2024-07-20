from .utils.graduation_check_util import GraduationCheckUtil
from ..models import LectureGroup, Condition, LectureCondition, LectureIdentification, LectureIdentificationLectureGroup, Prerequest

class GraduationCheckService:
    def check_graduation(self, year, tech, excel_file):
        # data
        data = {
            'lecture_condition_check': [],
            'essential_lecture_group_check': [],
            'total_credit_check': {},
            'prerequest_check': [],
            'grade_point_check': {}
        }
        
        condition = Condition.objects.get(year = year, tech = tech)

        user_lectures = GraduationCheckUtil.read_report_card(excel_file) # year, season, code, credit, grade
        user_lectures_codes = [user_lecture['code'] for user_lecture in user_lectures]

        # 1. 총 이수 최소 학점 확인
        total_credit = 0 
        
        for user_lecture in user_lectures:
            if(user_lecture['grade'] == 'F'):
                continue
            total_credit += user_lecture['credit']
        graduation_minimum_total_credit = condition.total_minimum_credit
        if total_credit < graduation_minimum_total_credit:
            data['total_credit_check']['ratio'] = f"{total_credit}/{graduation_minimum_total_credit}"
            data['total_credit_check']['value'] = False
        else:
            data['total_credit_check']['ratio'] = f"{total_credit}/{graduation_minimum_total_credit}"
            data['total_credit_check']['value'] = True
        
        # 2. 필수 강의 수강 여부 확인
        lecture_conditions = LectureCondition.objects.filter(condition = condition) # 2020학번 심화과정 졸업 요건들 중
        for lecture_condition in lecture_conditions: # 각각의 졸업 요건 안에,
            essential_lecture_group_list = list(LectureGroup.objects.filter(lecture_condition = lecture_condition, is_essential = True))
            result_list = [{lecture_group.lecture_group_name: False} for lecture_group in essential_lecture_group_list] # 각각의 필수 강의 그룹에 대해 False로 초기화된 리스트 생성
            for essential_lecture_group in essential_lecture_group_list: # 속해있는 필수 강의 그룹에 대해
                essential_lecture_group_lectures = LectureIdentificationLectureGroup.objects.filter(lecture_group=essential_lecture_group).select_related('lecture_identification') # 해당 필수 강의 그룹에 실제 맵핑되는 강의들을 essential_lecture_group_lectures에 저장
                for essential_lecture_group_lecture in essential_lecture_group_lectures: # 각각의 강의 하나하나마다
                    mandatory_lecture = LectureIdentification.objects.get(id = essential_lecture_group_lecture.lecture_identification.id) # 사용자의 수강 강의 목록에 해당 강의가 있는지 확인
                    if mandatory_lecture.code in user_lectures_codes: # 있다면
                        result_list[essential_lecture_group_list.index(essential_lecture_group)][essential_lecture_group.lecture_group_name] = True # 해당 필수 강의 그룹에 대해 True로 변경
                        break # 다음 필수 강의 그룹으로 넘어감
        # result_list를 새로운 포맷으로 변환
        for result in result_list:
            for group_name, check_value in result.items():
                essential_status = {
                    "name": group_name,
                    "value": check_value
                }
                data['essential_lecture_group_check'].append(essential_status)

        # 3. 선수과목 수강 여부 확인
        if Prerequest.objects.all().count() == 0:
            data['prerequest_check'].append({
                "name": "선수과목 정보가 없습니다.",
                "value": True
            })
        else:
            for user_lecture in user_lectures:
                lecture_identification = LectureIdentification.objects.get(year = user_lecture['year'], season = user_lecture['season'], code = user_lecture['code'], credit = user_lecture['credit'])
                lecture_lecture_group = LectureIdentificationLectureGroup.objects.get(lecture_identification = lecture_identification)
                lecture_group = LectureGroup.objects.get(id = lecture_lecture_group.lecture_group.id)
                prerequests = Prerequest.objects.filter(lecture_group = lecture_group)
                result_list = [{prerequest.prerequest_lecture_group.lecture_group_name: False} for prerequest in prerequests]
                for prerequest in prerequests:
                    prerequests_list = list(prerequests)
                    prerequest_lecture_group_lectures = LectureIdentificationLectureGroup.objects.filter(lecture_group = prerequest.prerequest_lecture_group)
                    for prerequest_lecture_group_lecture in prerequest_lecture_group_lectures:
                        prerequest_lecture = LectureIdentification.objects.get(id = prerequest_lecture_group_lecture.lecture.id)
                        if prerequest_lecture.code in user_lectures_codes:
                            result_list[prerequests_list.index(prerequest)][prerequest.prerequest_lecture_group.lecture_group_name] = True
                            break

                    for result in result_list:
                        for group_name, check_value in result.items():
                            prerequest_status = {
                                "name": group_name,
                                "value": check_value
                            }
                            data['prerequest_check'].append(prerequest_status)

        # 4. 각각의 졸업 요건 만족 여부 확인
        lecture_conditions = LectureCondition.objects.filter(condition=condition)
        for lecture_condition in lecture_conditions:
            satisfying_credit = 0
            for user_lecture in user_lectures:
                try:
                    lecture_identification = LectureIdentification.objects.get(year=user_lecture['year'], season=user_lecture['season'], code=user_lecture['code'], credit=user_lecture['credit'])
                    lecture_identification_lecture_group = LectureIdentificationLectureGroup.objects.get(lecture_identification=lecture_identification)
                except LectureIdentification.DoesNotExist:
                    data[f"{user_lecture['code']}_missing"] = f"Lecture with year={user_lecture['year']}, season={user_lecture['season']}, code={user_lecture['code']}, credit={user_lecture['credit']} does not exist."
                    continue
                except LectureIdentificationLectureGroup.DoesNotExist:
                    continue  # lecture_identification_lecture_group이 없으면 다음 요소로 넘어감
                
                lecture_group = LectureGroup.objects.get(id=lecture_identification_lecture_group.lecture_group.id)
                if lecture_group.lecture_condition_id == lecture_condition.id:  # 비교 수정
                    satisfying_credit += user_lecture['credit']
            
            condition_status = {
                "name": lecture_condition.condition_name,
                "ratio": f"{satisfying_credit}/{lecture_condition.minimum_credit}",
                "value": satisfying_credit >= lecture_condition.minimum_credit
            }
            data["lecture_condition_check"].append(condition_status)


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
            data['grade_point_check']['ratio'] = f"{user_lecture_score / user_total_credit}"
            data['grade_point_check']['value'] = False
        else:
            data['grade_point_check']['ratio'] = f"{user_lecture_score / user_total_credit}"
            data['grade_point_check']['value'] = True
        # 결과 JSON 반환
        return data

    
