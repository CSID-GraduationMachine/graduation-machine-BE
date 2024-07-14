from rest_framework import serializers
from .models import GraduationRequirementsDetail

class GraduationRequirementsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraduationRequirementsDetail
        fields = '__all__'
