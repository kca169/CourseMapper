from django.db import models

# Refs: [8]

# Basic course model.
class Course(models.Model):

    number_str = models.CharField(max_length=12, default="TEST 123")  ##This is not a IntegerField because some courses contain letters (ex. CMPT 105W). See course_number.
    description = models.CharField(max_length=1000, default="This is an example description")

    code = models.CharField(max_length=5, default="TEST") ## The (usually) four letter string that preceds the course number
    number = models.IntegerField()

    prerequisites = models.ForeignKey('self', null=True, on_delete=models.CASCADE) # Find alterative to CASCADE

    def __str__(self):
        return self.number_str + self.description
    
    pass
