from django.db import models

# Refs: [8]

# Basic course model.
class Course(models.Model):

    title = models.CharField(max_length = 50, default='This is an example title')
    number_str = models.CharField(max_length=12, default="TEST 123")  ##This is not a IntegerField because some courses contain letters (ex. CMPT 105W). See course_number.
    description = models.CharField(max_length=1000, default="This is an example description")
    code = models.CharField(max_length=5, default="TEST") ## The (usually) four letter string that preceds the course number
    number = models.IntegerField(default = 123)
    year = models.IntegerField(default=2021)
    semester = models.CharField(max_length=15, default="New example")

    # Signature is all the str fields concatenated together. with it being set to unique, this prevents duplicates... hopefully.
    signature = models.CharField(max_length=1500, default="Change this.", unique=True)

    # prerequisites = models.CharField(max_length=1000, default = "This is an example of a prerequisite")
    prerequisites = models.ForeignKey('self', null=True, on_delete=models.CASCADE) # Find alterative to CASCADE
    
    # units = models.CharField(max_length=10, default="3")
    
    units = models.IntegerField()
    grade = models.CharField(max_length=3, default="NI") # NI == not inputted
    
    
    def __str__(self):
        return self.number_str + self.description
    
    pass
