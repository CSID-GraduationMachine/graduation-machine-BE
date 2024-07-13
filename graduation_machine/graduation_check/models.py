from django.db import models

class GraduationRequirements(models.Model):
    year = models.IntegerField()
    tech = models.CharField(max_length=255)
    total_minimum_credit = models.IntegerField()

    def __str__(self):
        return f"{self.requirements_name} ({self.year})"

class GraduationRequirementsDetail(models.Model):
    gr = models.ForeignKey(GraduationRequirements, null=True, blank=True, on_delete=models.SET_NULL)
    requirements_name = models.CharField(max_length=255)
    minimum_credit = models.IntegerField()

class LectureGroup(models.Model):
    grd = models.ForeignKey(GraduationRequirementsDetail, null=True, blank=True, on_delete=models.SET_NULL)
    lecture_group_name = models.CharField(max_length=255)
    is_mandatory = models.BooleanField(default=False)

    def __str__(self):
        return self.lecture_group_name

class Lecture(models.Model):
    year = models.IntegerField()
    season = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    credit = models.IntegerField()
    lecture_groups = models.ManyToManyField(LectureGroup, through='LectureLectureGroup')

    def __str__(self):
        return f"{self.code} - {self.year} {self.season}"

class LectureLectureGroup(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    lecture_group = models.ForeignKey(LectureGroup, on_delete=models.CASCADE)

class Prerequest(models.Model):
    lecture_group = models.ForeignKey(LectureGroup, on_delete=models.CASCADE, related_name='main_lecture_group')
    prerequest_lecture_group = models.ForeignKey(LectureGroup, on_delete=models.CASCADE, related_name='prerequest_lecture_group')

    def __str__(self):
        return f"{self.lecture_group} requires {self.prerequest_lecture_group}"

class CommonLectureGroup(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    common_group_name = models.CharField(max_length=255)