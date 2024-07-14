from rest_framework import serializers
from .models import GraduationRequirementsDetail
from .models import LectureGroup
from .models import Lecture
from .models import Prerequest

class GraduationRequirementsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraduationRequirementsDetail
        fields = '__all__'

class LectureGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureGroup
        fields = '__all__'

class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = '__all__'


class PrerequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prerequest
        fields = '__all__'