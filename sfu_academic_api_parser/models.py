from django.db import models

# Basic course model.
class Course(models.Model):

    number_str = models.CharField(max_length=12, default="TEST 123")  ##This is not a IntegerField because some courses contain letters (ex. CMPT 105W). See course_number.
    description = models.CharField(max_length=1000, default="This is an example description")

    code = models.CharField(max_length=5) ## The (usually) four letter string that preceds the course number
    number = models.IntegerField()

    # prerequisites = ??? # NEED TO FIND A datatype / relationship system for this.

    def __str__(self):
        return self.department + self.number 
    
    pass
