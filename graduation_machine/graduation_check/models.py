from django.db import models


class Condition(models.Model):

    year = models.IntegerField()
    tech = models.CharField(max_length=255)
    total_minimum_credit = models.IntegerField()

    def __str__(self):
        return f"{self.year}학년도 -{self.tech}과정"


class LectureCondition(models.Model):

    condition = models.ForeignKey(Condition, null=True, blank=True, on_delete=models.SET_NULL)
    condition_name = models.CharField(max_length=255)
    minimum_credit = models.IntegerField()

    def __str__(self):
        return self.condition_name


class LectureGroup(models.Model):
    lecture_condition = models.ForeignKey(LectureCondition, null=True, blank=True, on_delete=models.SET_NULL)
    lecture_group_name = models.CharField(max_length=255)
    is_essential = models.BooleanField(default=False)

    def __str__(self):
        return self.lecture_group_name


class LectureIdentification(models.Model):

    year = models.IntegerField()
    season = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=255, default='')
    credit = models.IntegerField()
    lecture_groups = models.ManyToManyField(LectureGroup, through='LectureIdentificationLectureGroup')

    def __str__(self):
        return f"{self.code} - {self.year} {self.season} - {self.name}"


class LectureIdentificationLectureGroup(models.Model):
    lecture_identification = models.ForeignKey(LectureIdentification, on_delete=models.CASCADE)
    lecture_group = models.ForeignKey(LectureGroup, on_delete=models.CASCADE)

    def __str__(self):
        return f" {self.lecture_group.lecture_group_name} - {self.lecture_identification.name} - {self.lecture_identification.code}"

class Prerequest(models.Model):
    lecture_group = models.ForeignKey(LectureGroup, on_delete=models.CASCADE, related_name='main_lecture_group')
    prerequest_lecture_group = models.ForeignKey(LectureGroup, on_delete=models.CASCADE,
                                                 related_name='prerequest_lecture_group')

    def __str__(self):
        return f"{self.lecture_group.lecture_group_name}의 선이수 {self.prerequest_lecture_group.lecture_group_name}"


class CommonLectureGroup(models.Model):
    common_group_name = models.CharField(max_length=255)

    def __str__(self):
        return self.common_group_name

class CommonLectureGroupLectureIdentification(models.Model):
    common_lecture_group = models.ForeignKey(CommonLectureGroup, on_delete=models.CASCADE)
    lecture_identification = models.ForeignKey(LectureIdentification, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.common_lecture_group.common_group_name} - {self.lecture_identification.name} - {self.lecture_identification.code}"