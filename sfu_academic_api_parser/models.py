from django.db import models

class Course(models.Model):
    course_code = models.CharField(max_length=25)
    number_raw = models.CharField(max_length=10)  ##This is not a IntegerField because some courses contain letters (ex. CMPT 105W)
    number_extracted = models.IntegerField(max_length=10)
    is_w_course = models.BooleanField()
    units = models.IntegerField()
    description = models.CharField(max_length=1000)

    def __str__(self):
        return to_upper(self.department) + self.number 
