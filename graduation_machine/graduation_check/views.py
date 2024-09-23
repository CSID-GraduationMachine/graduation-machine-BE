from rest_framework import viewsets, mixins, views
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .serializers import (
    LectureConditionSerializer,
    LectureGroupSerializer,
    LectureIdentificationLectureGroupSerializer,
    PrerequestSerializer,
    CommonLectureGroupSerializer,
    ConditionSerializer,
    CommonLectureGroupLectureIdentificationSerializer,
    MultiLectureGroupSerializer
)

from .services.common_lecture_group_lecture_identification_service import CommonLectureGroupLectureIdentificationService
from .services.condition_service import ConditionService
from .services.lecture_condition_service import LectureConditionService
from .services.lecture_identification_lecture_group_service import LectureIdentificationLectureGroupService
from .services.lecture_group_service import LectureGroupService
from .services.prerequest_service import PrerequestService
from .services.common_lecture_group_service import CommonLectureGroupService
from .services.graduation_check_service import GraduationCheckService
from .services.lecture_identification_service import LectureIdentificationService
from .services.multi_lecture_group_service import MultiLectureGroupService

class ConditionViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin
):
    serializer_class = ConditionSerializer

    def list(self, request, *args, **kwargs):
        """
        졸업 요건 조회
        """
        requirements = ConditionService.get_conditions()
        return Response({"success": True, "data": ConditionSerializer(requirements, many=True).data, "error": None})

    def create(self, request, *args, **kwargs):
        """
        졸업 요건 생성
        """
        year = request.data.get('year')
        tech = request.data.get('tech')
        total_minimum_credit = request.data.get('total_minimum_credit')
        ConditionService.create_condition(year, tech, total_minimum_credit)
        return Response({"success": True, "data": None, "error": None})

    def destroy(self, request, *args, **kwargs):
        """
        졸업 요건 삭제
        """
        condition_id = kwargs.get('conditions_pk')
        ConditionService.delete_condition(condition_id)
        return Response({"success": True, "data": None, "error": None})

    def update(self, request, *args, **kwargs):
        """
        졸업 요건 수정
        """
        condition_id = kwargs.get('conditions_pk')
        year = request.data.get('year')
        tech = request.data.get('tech')
        total_minimum_credit = request.data.get('total_minimum_credit')
        ConditionService.update_condition(condition_id, year, tech, total_minimum_credit)
        return Response({"success": True, "data": None, "error": None})

class LectureConditionViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin
    ):

    serializer_class = LectureConditionSerializer

    def list(self, request, *args, **kwargs):
        """
        졸업 요건 상세 조회
        """
        condition_id = kwargs.get('conditions_pk')
        details = LectureConditionService.get_lecture_conditions(condition_id)
        total_minimum_credit = ConditionService.get_total_minimum_credit(condition_id)
        
        serialized_data = LectureConditionSerializer(details, many=True).data
        
        response_data = {
            "success": True,
            "data": {
                "total_minimum_credit": total_minimum_credit,
                "requirements": serialized_data
            },
            "error": None
        }

        return Response(response_data)
        
    def create(self, request, *args, **kwargs):
        """
        졸업 요건 상세 생성
        """
        condition_id = kwargs.get('conditions_pk')
        lecture_condition_name = request.data.get('name')
        minimum_credit = request.data.get('minimum_credit')
        LectureConditionService.create_lecture_condition(condition_id, lecture_condition_name, minimum_credit)
        return Response({"success": True, "data": None, "error": None})
        
    def update(self, request, *args, **kwargs):
        """
        졸업 요건 상세 수정
        """
        lecture_condition_id = kwargs.get('lecture_conditions_pk')
        lecture_condition_name = request.data.get('name')
        minimum_credit = request.data.get('minimum_credit')
        LectureConditionService.update_lecture_condition(lecture_condition_id, lecture_condition_name, minimum_credit)
        return Response({"success": True, "data": None, "error": None})
    
    def destroy(self, request, *args, **kwargs):
        """
        졸업 요건 상세 삭제
        """
        lecture_condition_id = kwargs.get('lecture_conditions_pk')
        LectureConditionService.delete_lecture_condition(lecture_condition_id)
        return Response({"success": True, "data": None, "error": None})


class LectureGroupViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin
    ):
    serializer_class = LectureGroupSerializer

    def list(self, request, *args, **kwargs):
        """
        선택한 졸업 요건 상세에 포함된 강의 그룹 조회
        """
        lecture_condition_id = kwargs.get('lecture_conditions_pk')
        lecture_groups = LectureGroupService.get_lecture_groups(lecture_condition_id)
        return Response({"success": True, "data": LectureGroupSerializer(lecture_groups, many=True).data, "error": None})
    def create(self, request, *args, **kwargs):
        """
        선택한 졸업 요건 상세에 포함된 강의 그룹 생성
        """
        lecture_condition_id = kwargs.get('lecture_conditions_pk')
        lecture_group_name = request.data.get('name')
        is_essential = request.data.get('is_essential')
        LectureGroupService.create_lecture_group(lecture_condition_id, lecture_group_name, is_essential)
        return Response({"success": True, "data": None, "error": None})
    def update(self, request, *args, **kwargs):
        """
        선택한 졸업 요건 상세에 포함된 강의 그룹 수정
        """
        lecture_group_id = kwargs.get('groups_pk')
        lecture_group_name = request.data.get('name')
        is_essential = request.data.get('is_essential')
        maximum_number = request.data.get('maximum_number')
        minimum_number = request.data.get('minimum_number')
        LectureGroupService.update_lecture_group(lecture_group_id, lecture_group_name, is_essential, maximum_number, minimum_number)
        return Response({"success": True, "data": None, "error": None})
    def destroy(self, request, *args, **kwargs):
        """
        선택한 졸업 요건 상세에 포함된 강의 그룹 삭제
        """
        lecture_group_id = kwargs.get('groups_pk')
        LectureGroupService.delete_lecture_group(lecture_group_id)
        return Response({"success": True, "data": None, "error": None})

class MultiLectureGroupViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin
    ):
    serializer_class = MultiLectureGroupSerializer

    def create(self, request, *args, **kwargs):
        """
        선택한 강의 그룹에 다중 강의 그룹 생성
        """
        lecture_group_id = kwargs.get('groups_pk')
        MultiLectureGroupService.create_multi_lecture_group(lecture_group_id)
        return Response({"success": True, "data": None, "error": None})

    def destroy(self, request, *args, **kwargs):
        """
        선택한 강의 그룹에 다중 강의 그룹 삭제
        """
        multi_lecture_group_id = kwargs.get('multi_pk')
        MultiLectureGroupService.delete_multi_lecture_group(multi_lecture_group_id)
        return Response({"success": True, "data": None, "error": None})

    def update(self, request, *args, **kwargs):
        """
        선택한 강의 그룹에 다중 강의 그룹 수정
        """
        multi_lecture_group_id = kwargs.get('multi_pk')
        minimum_number = request.data.get('minimum_number')
        maximum_number = request.data.get('maximum_number')
        MultiLectureGroupService.update_multi_lecture_group(multi_lecture_group_id, minimum_number, maximum_number)
        return Response({"success": True, "data": None, "error": None})

    def list(self, request, *args, **kwargs):
        """
        선택한 강의 그룹에 다중 강의 그룹 조회
        """
        lecture_group_id = kwargs.get('groups_pk')
        multi_lecture_groups = MultiLectureGroupService.get_multi_lecture_groups(lecture_group_id)
        return Response({"success": True, "data": MultiLectureGroupSerializer(multi_lecture_groups, many=False).data, "error": None})

class LectureIdentificationLectureGroupViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin
    ):
    serializer_class = LectureIdentificationLectureGroupSerializer

    def list(self, request, *args, **kwargs):
        """
        선택한 강의 그룹의 강의 조회
        """
        lecture_group_id = kwargs.get('groups_pk')
        orderby = request.query_params.get('orderby', 'year')  # 기본값 'year'
        sorttype = request.query_params.get('sorttype', 'asc')  # 기본값 'asc'
        lecture_identification_lecturegroups = LectureIdentificationLectureGroupService.get_lecture_identification_lecturegroups(lecture_group_id, orderby, sorttype)
        return Response({"success": True, "data": LectureIdentificationLectureGroupSerializer(lecture_identification_lecturegroups, many=True).data, "error": None})
    def create(self, request, *args, **kwargs):
        """
        선택한 강의 그룹의 강의 생성. keyword가 있을 경우 해당 keyword로 강의 검색하여 해당되는 강의 모두 추가
        """
        type = self.request.query_params.get('type', 'none')  # 기본값 'none'
        keyword = request.data.get('keyword')
        lecture_group_id = kwargs.get('groups_pk')
        LectureIdentificationLectureGroupService.create_lecture_identification_lecturegroup(lecture_group_id, type, keyword)
        return Response({"success": True, "data": None, "error": None})
    def destroy(self, request, *args, **kwargs):
        """
        선택한 강의 그룹의 강의 삭제
        """
        lecture_id = kwargs.get('lectures_pk')
        LectureIdentificationLectureGroupService.delete_lecture_identification_lecturegroup(lecture_id)
        return Response({"success": True, "data": None, "error": None})
    


class PrerequestViewSet(viewsets.GenericViewSet, 
                        mixins.ListModelMixin, 
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin):
    serializer_class = PrerequestSerializer
    def list(self, request, *args, **kwargs):
        """
        선이수 조회
        """
        lecture_group_id = kwargs.get('groups_pk')
        prerequests = PrerequestService.get_prerequests(lecture_group_id)

        response_data = {
            "success": True,
            "data": PrerequestSerializer(prerequests, many=True).data,
            "error": None
        }
        return Response(response_data)
    
    def create(self, request, *args, **kwargs):
        """
        선이수 생성
        """
        lecture_group_id = kwargs.get('groups_pk')
        prerequst_lecture_group_id = request.data.get('id')
        prerequest_year = request.data.get('year')
        if prerequest_year == 'all':
            prerequest_year = 10000
        PrerequestService.create_prerequest(lecture_group_id, prerequest_year, prerequst_lecture_group_id)
        return Response({"success": True, "data": None, "error": None})
    
    def destroy(self, request, *args, **kwargs):
        """
        선이수 삭제
        """
        id = kwargs.get('prerequests_pk')
        PrerequestService.delete_prerequest(id)
        return Response({"success": True, "data": None, "error": None})
    


class CommonLectureGroupViewSet(viewsets.GenericViewSet, 
                                mixins.ListModelMixin, 
                                mixins.CreateModelMixin, 
                                mixins.DestroyModelMixin,
                                mixins.UpdateModelMixin):
    
    serializer_class = CommonLectureGroupSerializer

    def list(self, request, *args, **kwargs):
        """
        공통 강의 그룹 조회
        """
        common_lectures = CommonLectureGroupService.get_all_common_lectures()
        return Response({"success": True, "data": CommonLectureGroupSerializer(common_lectures, many=True).data, "error": None})

    def create(self, request, *args, **kwargs):
        """
        공통 강의 그룹 생성
        """
        common_group_name = request.data.get('name')
        CommonLectureGroupService.create_common_lecture_group(common_group_name)
        return Response({"success": True, "data": None, "error": None})
    
    def update(self, request, *args, **kwargs):
        """
        공통 강의 그룹 수정
        """
        common_lecture_group_id = kwargs.get('groups_pk')
        common_group_name = request.data.get('name')
        CommonLectureGroupService.update_common_lecture_group(common_lecture_group_id, common_group_name)
        return Response({"success": True, "data": None, "error": None})

    def destroy(self, request, *args, **kwargs):
        """
        공통 강의 그룹 삭제
        """
        common_lecture_group_id = kwargs.get('groups_pk')
        CommonLectureGroupService.delete_common_lecture_group(common_lecture_group_id)
        return Response({"success": True, "data": None, "error": None})
    
class CommonLectureGroupLectureIdentificationViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin
    ):
    serializer_class = CommonLectureGroupLectureIdentificationSerializer

    def list(self, request, *args, **kwargs):
        """
        공통 강의 그룹에 포함된 강의 조회
        """
        orderby = request.query_params.get('orderby', 'year')  # 기본값 'year'
        sorttype = request.query_params.get('sorttype', 'asc')  # 기본값 'asc'

        common_lecture_group_id = kwargs.get('groups_pk')
        common_lecture_group_lecture = CommonLectureGroupLectureIdentificationService.get_lectures(common_lecture_group_id, orderby, sorttype)
        return Response({"success": True, "data": CommonLectureGroupLectureIdentificationSerializer(common_lecture_group_lecture, many=True).data, "error": None})
    def create(self, request, *args, **kwargs):
        """
        공통 강의 그룹에 포함된 강의 생성
        """
        common_lecture_group_id = kwargs.get('groups_pk')
        type = self.request.query_params.get('type', 'none')  # 기본값 'none'
        keyword = request.data.get('keyword')
        CommonLectureGroupLectureIdentificationService.create_common_lecture_group_lecture_identification(common_lecture_group_id, type, keyword)
        return Response({"success": True, "data": None, "error": None})
    def destroy(self, request, *args, **kwargs):
        """
        공통 강의 그룹에 포함된 강의 삭제
        """

        common_lecture_group_lecture_identification_id = kwargs.get('lectures_pk')
        CommonLectureGroupLectureIdentificationService.delete_common_lecture_group_lecture_identification(common_lecture_group_lecture_identification_id)
        return Response({"success": True, "data": None, "error": None})

class LectureIdentificationAPIView(views.APIView):
    def get(self, request, *args, **kwargs):
        orderby = request.query_params.get('orderby', 'year')  # 기본값 'year'
        sorttype = request.query_params.get('sorttype', 'asc')  # 기본값 'asc'

        try:
            data = LectureIdentificationService.get_lecture_identifications(orderby, sorttype)
            return Response({"success": True, "data": data, "error": None})
        except ValueError as e:  # orderby 파라미터가 유효하지 않은 경우
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:  # 다른 예외 처리
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LectureGroupForAddPrerequestAPIView(views.APIView):
    def get(self, request, *args, **kwargs):
        lecture_condition_id = kwargs.get('lecture_conditions_pk')
        lecture_group_id = kwargs.get('groups_pk')
        lecture_groups = LectureGroupService.get_lecture_groups_for_add_prerequest(lecture_condition_id, lecture_group_id)
        return Response({"success": True, "data": LectureGroupSerializer(lecture_groups, many=True).data, "error": None})

class LectureIdentificationLectureGroupForCommonLectureGroupAPIView(views.APIView):
    def post(self, request, *args, **kwargs):
        lecture_group_id = kwargs.get('groups_pk')
        common_lecture_group_id = request.data.get('id')
        LectureIdentificationLectureGroupService.create_lecture_identification_lecturegroup_for_common_lecture_group(lecture_group_id, common_lecture_group_id)
        return Response({"success": True, "data": None, "error": None})

class GraduationCheckAPIView(views.APIView):

    def post(self, request, *args, **kwargs):
        year = self.request.query_params.get('year')
        tech = self.request.query_params.get('tech')
        excel_file = request.FILES.get('file')
        password = request.data.get('password', None)

        if not excel_file.name.endswith('.xlsx'):
            return JsonResponse({'error': 'File is not xlsx format'}, status=400)
        
        return Response({"success": True, "data": GraduationCheckService().check_graduation(year, tech, excel_file, password), "error": None})
