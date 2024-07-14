from rest_framework import serializers
from .models import GraduationRequirementsDetail

class GraduationRequirementsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraduationRequirementsDetail
        fields = '__all__'


from rest_framework import serializers
from .models import LectureGroup

class LectureGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureGroup
        fields = '__all__'
