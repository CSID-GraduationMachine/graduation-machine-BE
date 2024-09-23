from rest_framework import serializers
from .models import LectureCondition
from .models import LectureGroup
from .models import LectureIdentification
from .models import Prerequest
from .models import CommonLectureGroup
from .models import Condition
from .models import LectureIdentificationLectureGroup
from .models import CommonLectureGroupLectureIdentification
from .models import MultiLectureGroup

class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = '__all__'

class LectureConditionSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = LectureCondition
        fields = ['id', 'name', 'minimum_credit']

    def get_name(self, obj):
        return obj.condition_name

class LectureGroupSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    lectureConditionName = serializers.SerializerMethodField()
    lectureConditionId = serializers.SerializerMethodField()
    is_multi_lecture = serializers.SerializerMethodField()
    maximum_number = serializers.SerializerMethodField()
    minimum_number = serializers.SerializerMethodField()

    class Meta:
        model = LectureGroup
        fields = ['id', 'name', 'is_essential', 'is_multi_lecture', 'maximum_number', 'minimum_number', 'lectureConditionName', 'lectureConditionId']
    def get_name(self, obj):
        return obj.lecture_group_name
    def get_lectureConditionName(self, obj):
        return obj.lecture_condition.condition_name
    def get_lectureConditionId(self, obj):
        return obj.lecture_condition.id
    def get_is_multi_lecture(self, obj):
        if obj.multi_lecture_group is None:
            return False
        return True
    def get_maximum_number(self, obj):
        if obj.multi_lecture_group is None:
            return None
        return obj.multi_lecture_group.maximum_number
    def get_minimum_number(self, obj):
        if obj.multi_lecture_group is None:
            return None
        return obj.multi_lecture_group.minimum_number

class MultiLectureGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultiLectureGroup
        fields = ['id', 'minimum_number', 'maximum_number']

class LectureIdentificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureIdentification
        fields = ['id', 'year', 'season', 'code', 'name', 'credit']

class LectureIdentificationLectureGroupSerializer(serializers.ModelSerializer):
    year = serializers.SerializerMethodField()
    season = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    credit = serializers.SerializerMethodField()

    class Meta:
        model = LectureIdentificationLectureGroup
        fields = ['id', 'year', 'season', 'code', 'name', 'credit']

    def get_year(self, obj):
        return obj.lecture_identification.year
    def get_season(self, obj):
        return obj.lecture_identification.season
    def get_code(self, obj):
        return obj.lecture_identification.code
    def get_name(self, obj):
        return obj.lecture_identification.name
    def get_credit(self, obj):
        return obj.lecture_identification.credit

class PrerequestSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    class Meta:
        model = Prerequest
        fields = ['id', 'year', 'name']

    def get_name(self, obj):
        return obj.prerequest_lecture_group.lecture_group_name
    def get_year(self, obj):
        year = obj.year
        if year == 10000:
            return "all"
        return year

class CommonLectureGroupSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = CommonLectureGroup
        fields = ['id', 'name']
    def get_name(self, obj):
        return obj.common_group_name

class CommonLectureGroupLectureIdentificationSerializer(serializers.ModelSerializer):
    year = serializers.SerializerMethodField()
    season = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    credit = serializers.SerializerMethodField()

    class Meta:
        model = CommonLectureGroupLectureIdentification
        fields = ['id', 'year', 'season', 'code', 'name', 'credit']

    def get_year(self, obj):
        return obj.lecture_identification.year
    def get_season(self, obj):
        return obj.lecture_identification.season
    def get_code(self, obj):
        return obj.lecture_identification.code
    def get_name(self, obj):
        return obj.lecture_identification.name
    def get_credit(self, obj):
        return obj.lecture_identification.credit