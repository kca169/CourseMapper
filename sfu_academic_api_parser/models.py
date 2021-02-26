from django.db import models

# Refs : [3],[4],[5],[6]


'''
THE BASIC COURSE MODEL:

Things to add:
    WQB status
    ...
'''
# manager class for the courses
#class CourseExtractor(models.Manager):
 #   def extract_data(json_file):
  #      course = self.create()
   #     return course

class Course(models.Model):
    
    json_file = models.JSONField()

    dept_code = models.CharField(max_length=25)
    number_raw = models.CharField(max_length=10)  ##This is not initally IntegerField because some courses contain letters (ex. CMPT 105W)
    number_extracted = models.IntegerField() # This is the course number
    is_w_course = models.BooleanField()
    units = models.IntegerField()
    description = models.CharField(max_length=1000) 

    #def extract_data(json_file):
        #json_file.

    def __str__(self):
        return self.department + self.number 
