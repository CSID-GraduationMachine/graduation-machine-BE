from rest_framework import serializers
from .models import GraduationRequirementsDetail
from .models import LectureGroup
from .models import Lecture
from .models import Prerequest
from .models import CommonLectureGroup
from .models import GraduationRequirements
from .models import LectureLectureGroup
from .models import CommonLectureGroupLecture

class GraduationRequirementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraduationRequirements
        fields = '__all__'

class GraduationRequirementsDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = GraduationRequirementsDetail
        fields = ['id', 'requirements_name', 'minimum_credit']


class LectureGroupSerializer(serializers.ModelSerializer):
    is_essential = serializers.SerializerMethodField()
    class Meta:
        model = LectureGroup
        fields = ['id', 'lecture_group_name', 'is_essential']
    
    def get_is_essential(self, obj):
        return obj.is_mandatory

class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['id', 'year', 'season', 'code', 'name', 'credit']

class LectureLectureGroupSerializer(serializers.ModelSerializer):
    year = serializers.SerializerMethodField()
    season = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    credit = serializers.SerializerMethodField()

    class Meta:
        model = LectureLectureGroup
        fields = ['id', 'year', 'season', 'code', 'name', 'credit']

    def get_year(self, obj):
        return obj.lecture.year
    def get_season(self, obj):
        return obj.lecture.season
    def get_code(self, obj):
        return obj.lecture.code
    def get_name(self, obj):
        return obj.lecture.name
    def get_credit(self, obj):
        return obj.lecture.credit

class PrerequestSerializer(serializers.ModelSerializer):
    prerequest_lecture_name = serializers.SerializerMethodField()
    class Meta:
        model = Prerequest
        fields = ['id', 'lecture_group', 'prerequest_lecture_group', 'prerequest_lecture_name']

    def get_prerequest_lecture_name(self, obj):
        return obj.prerequest_lecture_group.lecture_group_name

class CommonLectureGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonLectureGroup
        fields = '__all__'

class CommonLectureGroupLectureSerializer(serializers.ModelSerializer):
    year = serializers.SerializerMethodField()
    season = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    credit = serializers.SerializerMethodField()

    class Meta:
        model = CommonLectureGroupLecture
        fields = ['id', 'year', 'season', 'code', 'name', 'credit']

    def get_year(self, obj):
        return obj.lecture.year
    def get_season(self, obj):
        return obj.lecture.season
    def get_code(self, obj):
        return obj.lecture.code
    def get_name(self, obj):
        return obj.lecture.name
    def get_credit(self, obj):
        return obj.lecture.credit