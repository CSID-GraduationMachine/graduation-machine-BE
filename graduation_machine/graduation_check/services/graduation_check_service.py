from .utils.graduation_check_util import GraduationCheckUtil
from ..models import LectureGroup, Condition, LectureCondition, LectureIdentification, LectureIdentificationLectureGroup, Prerequest

class GraduationCheckService:
    def check_graduation(self, year, tech, excel_file):
        # data
        data = {
            'lectureConditionList': [],
            'essential_lecture_group': [],
            'total_credit': {},
            'grade': {}
        }

        condition = Condition.objects.get(year = year, tech = tech)

        user_lectures = GraduationCheckUtil.read_report_card(excel_file) # year, season, code, credit, grade
        user_lectures_codes = [user_lecture['code'] for user_lecture in user_lectures]

        def get_grade_for_code(code):
            for lecture in user_lectures:
                if lecture['code'] == code:
                    return lecture['grade']
            return None

        # 1. 총 이수 최소 학점 확인
        total_credit = 0

        for user_lecture in user_lectures:
            if(user_lecture['grade'] == 'F'):
                continue
            total_credit += user_lecture['credit']
        graduation_minimum_total_credit = condition.total_minimum_credit
        if total_credit < graduation_minimum_total_credit:
            data['total_credit']['ratio'] = f"{total_credit}/{graduation_minimum_total_credit}"
            data['total_credit']['value'] = False
        else:
            data['total_credit']['ratio'] = f"{total_credit}/{graduation_minimum_total_credit}"
            data['total_credit']['value'] = True

        # 2. 필수 강의 수강 여부 확인
        lecture_conditions = LectureCondition.objects.filter(condition = condition) # 2020학번 심화과정 졸업 요건들 중
        for lecture_condition in lecture_conditions: # 각각의 졸업 요건 안에,
            essential_lecture_group_list = list(LectureGroup.objects.filter(lecture_condition = lecture_condition, is_essential = True))
            result_list = [{lecture_group.lecture_group_name: False} for lecture_group in essential_lecture_group_list] # 각각의 필수 강의 그룹에 대해 False로 초기화된 리스트 생성
            for essential_lecture_group in essential_lecture_group_list: # 속해있는 필수 강의 그룹에 대해
                essential_lecture_group_lectures = LectureIdentificationLectureGroup.objects.filter(lecture_group=essential_lecture_group).select_related('lecture_identification') # 해당 필수 강의 그룹에 실제 맵핑되는 강의들을 essential_lecture_group_lectures에 저장
                for essential_lecture_group_lecture in essential_lecture_group_lectures: # 각각의 강의 하나하나마다
                    essential_lecture = LectureIdentification.objects.get(id = essential_lecture_group_lecture.lecture_identification.id) # 사용자의 수강 강의 목록에 해당 강의가 있는지 확인
                    if essential_lecture.code in user_lectures_codes: # 있다면
                        result_list[essential_lecture_group_list.index(essential_lecture_group)][essential_lecture_group.lecture_group_name] = True # 해당 필수 강의 그룹에 대해 True로 변경
                        break # 다음 필수 강의 그룹으로 넘어감

            # result_list를 새로운 포맷으로 변환
            for result in result_list:
                for group_name, check_value in result.items():
                    essential_status = {
                        "name": group_name,
                        "value": check_value
                    }
                    data['essential_lecture_group'].append(essential_status)


        # 각각의 졸업 요건 만족 여부 확인
        lecture_conditions = LectureCondition.objects.filter(condition=condition) # 유저의 졸업 요건(몇학번인지, 어떤 과정인지)을 가져와서
        for lecture_condition in lecture_conditions:  # 해당 졸업요건에 속한 lecture_condition 하나하나들에 대해 반복

            # response에 필요한 틀 형성
            lecture_condition_id = lecture_condition.id
            lecture_condition_name = lecture_condition.condition_name
            lecture_condition_minimum_credit = lecture_condition.minimum_credit
            lecture_condition_passed_credit = 0
            lecture_group_list = []

            # lectureGroupList 형성
            lecture_groups = LectureGroup.objects.filter(
                lecture_condition=lecture_condition)  # 해당 lecture_condition에 속한 lecture_group들을 가져와서
            lecture_group_is_passed = False  # 수강 여부 + 선이수 만족 여부

            for lecture_group in lecture_groups:  # 각각의 lecture_group에 대해
                lecture_group_is_essential = lecture_group.is_essential
                lecture_group_lecture_identifications = LectureIdentificationLectureGroup.objects.filter(
                    lecture_group=lecture_group)  # 해당 lecture_group에 속한 lecture_identification들을 가져와서
                lecture_identification_item = None # lecture_identification_item 초기화
                prerequest_group_list= []
                for lecture_group_lecture_identification in lecture_group_lecture_identifications:  # 각각의 lecture_identification에 대해
                    if lecture_group_lecture_identification.lecture_identification.code in user_lectures_codes:  # 해당 lecture_identification의 수강 여부 확인.
                        lecture_condition_passed_credit += lecture_group_lecture_identification.lecture_identification.credit  # 해당 lecture_identification의 학점을 더함
                        grade = get_grade_for_code(lecture_group_lecture_identification.lecture_identification.code)
                        lecture_identification_item = {
                            "id": lecture_group_lecture_identification.lecture_identification.id,
                            "code": lecture_group_lecture_identification.lecture_identification.code,
                            "grade": grade,
                            "name": lecture_group_lecture_identification.lecture_identification.name,
                            "year": lecture_group_lecture_identification.lecture_identification.year,
                            "season": lecture_group_lecture_identification.lecture_identification.season,
                            "credit": lecture_group_lecture_identification.lecture_identification.credit
                        }

                        if Prerequest.objects.filter(
                                lecture_group=lecture_group).exists():  # 선이수가 존재하는지 확인. (수강 + 선이수 만족 -> lecture_group_is_passed = True)
                            prerequest_group_list = []  # prerequest_group_list 초기화
                            prerequests = Prerequest.objects.filter(lecture_group=lecture_group)
                            prerequests_count = prerequests.count()
                            for prerequest in prerequests:
                                lecture_identification_lecture_group = LectureIdentificationLectureGroup.objects.filter(
                                    lecture_group=prerequest.prerequest_lecture_group)
                                prerequest_lecture_codes = [lecture_identification_lecture_group.lecture_identification.code
                                                            for lecture_identification_lecture_group in
                                                            lecture_identification_lecture_group]
                                prerequest_check_data = {
                                    "id": prerequest.prerequest_lecture_group.id,
                                    "name": prerequest.prerequest_lecture_group.lecture_group_name,
                                    "status": any(code in user_lectures_codes for code in prerequest_lecture_codes)
                                }
                                prerequest_group_list.append(prerequest_check_data)  # 리스트에 추가
                                prerequests_count -= 1
                            if prerequests_count == 0 and grade != 'F':  # 선이수가 없는데 F가 아니라면
                                lecture_group_is_passed = True
                            else:
                                lecture_group_is_passed = False

                        elif grade != 'F':  # 선이수가 없다면
                            lecture_group_is_passed = True
                        else:
                            lecture_group_is_passed = False
                        break
                if lecture_identification_item:
                    lecture_group_list.append({
                        "id": lecture_group.id,
                        "name": lecture_group.lecture_group_name,
                        "isPassed": lecture_group_is_passed,
                        "isEssential": lecture_group_is_essential,
                        "lectureIdentificationItem": lecture_identification_item,
                        "preLectureGroupList": prerequest_group_list  # 리스트 추가
                    })
                else:
                    lecture_group_list.append({
                        "name": lecture_group.lecture_group_name,
                        "isPassed": lecture_group_is_passed,
                        "isEssential": lecture_group_is_essential,
                        "lectureIdentificationItem": {},
                        "prerequestGroupList": []  # 빈 리스트 추가
                    })

            if lecture_condition_passed_credit >= lecture_condition_minimum_credit:
                lecture_condition_is_passed = True
            else:
                lecture_condition_is_passed = False

            data['lectureConditionList'].append({
                "id": lecture_condition_id,
                "name": lecture_condition_name,
                "isPassed": lecture_condition_is_passed,
                "minimumCredit": lecture_condition_minimum_credit,
                "passedCredit": lecture_condition_passed_credit,
                "lectureGroupList": lecture_group_list
            })

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
            data['grade']['gpa'] = f"{user_lecture_score / user_total_credit}"
            data['grade']['isPassed'] = False
        else:
            data['grade']['gpa'] = f"{user_lecture_score / user_total_credit}"
            data['grade']['isPassed'] = True
        # 결과 JSON 반환
        return data


