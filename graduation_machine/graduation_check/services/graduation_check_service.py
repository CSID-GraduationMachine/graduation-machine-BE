from .utils.graduation_check_util import GraduationCheckUtil
from ..models import LectureGroup, Condition, LectureCondition, LectureIdentification, LectureIdentificationLectureGroup, Prerequest

class GraduationCheckService:
    def check_graduation(self, year, tech, excel_file, password):
        # data
        data = {
            'lectureConditionList': [],
            'essential_lecture_group': [],
            'total_credit': {},
            'grade': {}
        }

        condition = Condition.objects.get(year = year, tech = tech)
        if password == None:
            user_lectures = GraduationCheckUtil.read_report_card_mdrims(excel_file)
        else:
            user_lectures = GraduationCheckUtil.read_report_card_ndrims(excel_file, password) # year, season, code, credit, grade, name
        user_lectures_codes = [user_lecture['code'] for user_lecture in user_lectures]
        def get_user_lecture_for_code(code):
            for lecture in user_lectures:
                if lecture['code'] == code:
                    return lecture
            return None
        unfiltered_lectures = []
        for user_lecture in user_lectures:
            if not LectureIdentification.objects.filter(code=user_lecture['code']).exists():
                unfiltered_lectures.append({
                    'year': user_lecture['year'],
                    'season': user_lecture['season'],
                    'code': user_lecture['code'],
                    'name': user_lecture['name'],
                    'grade': user_lecture['grade'],
                    'credit': user_lecture['credit']
                })
                user_lectures.remove(user_lecture)
                user_lectures_codes.remove(user_lecture['code'])
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


        # 3. 각각의 졸업 요건 만족 여부 확인
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
                prerequest_group_list= []
                matching_lectures_identifications_temp = lecture_group_lecture_identifications.filter(lecture_identification__code__in=user_lectures_codes).select_related('lecture_identification')
                matching_lectures = matching_lectures_identifications_temp.filter(
                    lecture_identification__year__in=[
                        get_user_lecture_for_code(lecture_group_lecture_identification.lecture_identification.code)['year']
                        for lecture_group_lecture_identification in lecture_group_lecture_identifications
                        if get_user_lecture_for_code(lecture_group_lecture_identification.lecture_identification.code) is not None
                    ],
                    lecture_identification__season__in=[
                        get_user_lecture_for_code(lecture_group_lecture_identification.lecture_identification.code)['season']
                        for lecture_group_lecture_identification in lecture_group_lecture_identifications
                        if get_user_lecture_for_code(lecture_group_lecture_identification.lecture_identification.code) is not None
                    ]
                )
                if matching_lectures.exists() and lecture_group.multi_lecture_group is None: # 일반강의
                    lecture_condition_passed_credit += matching_lectures[0].lecture_identification.credit  # 해당 lecture_identification의 학점을 더함
                    grade = get_user_lecture_for_code(matching_lectures[0].lecture_identification.code)['grade']
                    lecture_identification_item = {
                        "id": matching_lectures[0].lecture_identification.id,
                        "year": matching_lectures[0].lecture_identification.year,
                        "season": matching_lectures[0].lecture_identification.season,
                        "code": matching_lectures[0].lecture_identification.code,
                        "name": matching_lectures[0].lecture_identification.name,
                        "grade": grade,
                        "credit": matching_lectures[0].lecture_identification.credit
                    }
                    if Prerequest.objects.filter(
                            lecture_group=lecture_group, year=matching_lectures[0].lecture_identification.year).exists() or \
                        Prerequest.objects.filter(lecture_group = lecture_group, year = 10000).exists():  # 선이수가 존재하는지 확인. (수강 + 선이수 만족 -> lecture_group_is_passed = True)
                        prerequest_group_list = []  # prerequest_group_list 초기화
                        if Prerequest.objects.filter(lecture_group=lecture_group, year=10000).exists():  # 선이수가 모든 년도에 대해 적용인 경우
                            prerequests = Prerequest.objects.filter(lecture_group=lecture_group, year=10000)  # 해당 lecture_group의 선이수들을 가져와서
                        else:
                            prerequests = Prerequest.objects.filter(lecture_group=lecture_group, year=matching_lectures[0].lecture_identification.year)  # 해당 lecture_group의 선이수들을 가져와서
                        prerequests_count = prerequests.count()
                        for prerequest in prerequests:
                            lecture_identification_lecture_group = LectureIdentificationLectureGroup.objects.filter(
                                lecture_group=prerequest.prerequest_lecture_group)
                            prerequest_lecture_codes = [lecture_identification_lecture_group.lecture_identification.code
                                                        for lecture_identification_lecture_group in
                                                        lecture_identification_lecture_group
                                                        if lecture_identification_lecture_group.lecture_identification.year <= prerequest.year]
                            prerequest_status = any(code in user_lectures_codes for code in prerequest_lecture_codes)
                            prerequest_check_data = {
                                "id": prerequest.prerequest_lecture_group.id,
                                "name": prerequest.prerequest_lecture_group.lecture_group_name,
                                "status": prerequest_status
                            }
                            prerequest_group_list.append(prerequest_check_data)  # 리스트에 추가
                            if prerequest_status:
                                prerequests_count -= 1
                        if prerequests_count == 0 and grade != 'F':  # 선이수가 없는데 F가 아니라면
                            lecture_group_is_passed = True
                        else:
                            lecture_group_is_passed = False

                    elif grade != 'F':  # 선이수가 없다면
                        lecture_group_is_passed = True
                    else:
                        lecture_group_is_passed = False

                    lecture_group_list.append({
                        "id": lecture_group.id,
                        "name": lecture_group.lecture_group_name,
                        "isPassed": lecture_group_is_passed,
                        "isEssential": lecture_group_is_essential,
                        "lectureIdentificationItem": lecture_identification_item,
                        "preLectureGroupList": prerequest_group_list  # 리스트 추가
                    })

                elif matching_lectures.exists() and lecture_group.multi_lecture_group is not None: # 개별연구 혹은 다중강의그룹
                    maximum_number = lecture_group.multi_lecture_group.maximum_number
                    minimum_number = lecture_group.multi_lecture_group.minimum_number
                    user_number = 0
                    lecture_identification_items=[]

                    for matching_lecture in matching_lectures:
                        grade = get_user_lecture_for_code(matching_lecture.lecture_identification.code)['grade']
                        if(grade != 'F'):
                            lecture_condition_passed_credit += matching_lecture.lecture_identification.credit
                            user_number += 1

                        lecture_identification_item = {
                            "id": matching_lecture.lecture_identification.id,
                            "year": matching_lecture.lecture_identification.year,
                            "season": matching_lecture.lecture_identification.season,
                            "code": matching_lecture.lecture_identification.code,
                            "name": matching_lecture.lecture_identification.name,
                            "grade": grade,
                            "credit": matching_lecture.lecture_identification.credit
                        }
                        lecture_identification_items.append(lecture_identification_item)
                    if Prerequest.objects.filter(
                            lecture_group=lecture_group, year=matching_lectures[0].lecture_identification.year).exists() or \
                            Prerequest.objects.filter(lecture_group = lecture_group, year = 10000).exists():  # 선이수가 존재하는지 확인. (수강 + 선이수 만족 -> lecture_group_is_passed = True)
                        prerequest_group_list = []  # prerequest_group_list 초기화
                        if Prerequest.objects.filter(lecture_group=lecture_group, year=10000).exists():  # 선이수가 모든 년도에 대해 적용인 경우
                            prerequests = Prerequest.objects.filter(lecture_group=lecture_group, year=10000)  # 해당 lecture_group의 선이수들을 가져와서
                        else:
                            prerequests = Prerequest.objects.filter(lecture_group=lecture_group, year=matching_lectures[0].lecture_identification.year)  # 해당 lecture_group의 선이수들을 가져와서
                        prerequests_count = prerequests.count()
                        for prerequest in prerequests:
                            lecture_identification_lecture_group = LectureIdentificationLectureGroup.objects.filter(
                                lecture_group=prerequest.prerequest_lecture_group)
                            prerequest_lecture_codes = [lecture_identification_lecture_group.lecture_identification.code
                                                        for lecture_identification_lecture_group in
                                                        lecture_identification_lecture_group
                                                        if lecture_identification_lecture_group.lecture_identification.year <= prerequest.year]
                            prerequest_status = any(code in user_lectures_codes for code in prerequest_lecture_codes)
                            prerequest_check_data = {
                                "id": prerequest.prerequest_lecture_group.id,
                                "name": prerequest.prerequest_lecture_group.lecture_group_name,
                                "status": prerequest_status
                            }
                            prerequest_group_list.append(prerequest_check_data)  # 리스트에 추가
                            if prerequest_status:
                                prerequests_count -= 1
                        if prerequests_count == 0 and user_number >= minimum_number and user_number <= maximum_number:  # 선이수를 다 들었고, 최소, 최대 강의 수 사이에 있다면
                            lecture_group_is_passed = True
                        else:
                            lecture_group_is_passed = False

                    elif user_number >= minimum_number and user_number <= maximum_number:  # 선이수가 없다면
                        lecture_group_is_passed = True
                    else:
                        lecture_group_is_passed = False

                    lecture_group_list.append({
                        "id": lecture_group.id,
                        "name": lecture_group.lecture_group_name,
                        "isPassed": lecture_group_is_passed,
                        "isEssential": lecture_group_is_essential,
                        "lectureIdentificationItem": lecture_identification_items,
                        "preLectureGroupList": prerequest_group_list  # 리스트 추가
                    })
                else:
                    lecture_group_list.append({
                        "id": lecture_group.id,
                        "name": lecture_group.lecture_group_name,
                        "isPassed": lecture_group_is_passed,
                        "isEssential": lecture_group_is_essential,
                        "lectureIdentificationItem": {},
                        "preLectureGroupList": []  # 빈 리스트 추가
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
        # 4. 일반교양 과목 확인, 필터링되지 않은 과목 확인
        general_education_lectures = []  # 일반교양 과목을 저장할 리스트 초기화
        all_lecture_conditions_lectures = set()  # 모든 강의 조건에 속하는 강의 코드 저장

        for lecture_condition in lecture_conditions:
            for lecture_group in lecture_condition.lecturegroup_set.all():
                for lecture in lecture_group.lectureidentification_set.all():
                    all_lecture_conditions_lectures.add(lecture.code)

        for user_lecture in user_lectures:
            if user_lecture['code'] not in all_lecture_conditions_lectures:
                general_education_lectures.append({
                    'year': user_lecture['year'],
                    'season': user_lecture['season'],
                    'code': user_lecture['code'],
                    'name': user_lecture['name'],
                    'grade': user_lecture['grade'],
                    'credit': user_lecture['credit']
                })
        data['generalEducation'] = general_education_lectures  # 최종 데이터 구조에 일반교양 섹션 추가
        data['unfilteredLectures'] = unfiltered_lectures  # 최종 데이터 구조에 필터링되지 않은 섹션 추가

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

