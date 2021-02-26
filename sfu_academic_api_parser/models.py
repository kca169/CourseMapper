from django.db import models

# Refs : [3],[4], 


'''
THE BASIC COURSE MODEL:

Things to add:
    WQB status
'''

class Course(models.Model):
    
    dept_code = models.CharField(max_length=25)
    number_raw = models.CharField(max_length=10)  ##This is not initally IntegerField because some courses contain letters (ex. CMPT 105W)
    number_extracted = models.IntegerField() # This is the course number
    is_w_course = models.BooleanField()
    units = models.IntegerField()
    description = models.CharField(max_length=1000)


    def __str__(self):
        return self.department + self.number 
