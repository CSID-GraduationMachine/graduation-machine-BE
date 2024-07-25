from django.contrib import admin
from .models import CommonLectureGroup, CommonLectureGroupLectureIdentification, Condition, LectureCondition, LectureGroup, LectureIdentification, LectureIdentificationLectureGroup, Prerequest

# Register your models here.
admin.site.register(CommonLectureGroup)
admin.site.register(CommonLectureGroupLectureIdentification)
admin.site.register(Condition)
admin.site.register(LectureCondition)
admin.site.register(LectureGroup)
admin.site.register(LectureIdentification)
admin.site.register(LectureIdentificationLectureGroup)
admin.site.register(Prerequest)